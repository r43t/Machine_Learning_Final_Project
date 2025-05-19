import numpy as np
import torch
import torch.nn as nn
import joblib
import pickle
import pandas as pd
import random
import os

# === Define model directory ===
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
MODEL_DIR = os.path.abspath(MODEL_DIR)

# Load Random Forest model
rf_model = joblib.load(os.path.join(MODEL_DIR, "rf_model.pkl"))

# Load XGBoost model
xgb_model = joblib.load(os.path.join(MODEL_DIR, "xgboost_model.pkl"))

# Load MLP model class
class DetailedMLP(nn.Module):
   def __init__(self, input_size, output_size):
      super(DetailedMLP, self).__init__()
      self.net = nn.Sequential(
         nn.Linear(input_size, 512),
         nn.BatchNorm1d(512),
         nn.ReLU(),
         nn.Dropout(0.4),

         nn.Linear(512, 256),
         nn.ReLU(),
         nn.Dropout(0.3),

         nn.Linear(256, 128),
         nn.BatchNorm1d(128),
         nn.ReLU(),

         nn.Linear(128, output_size)
      )
   def forward(self, x):
      return self.net(x)

# Load MLP test tensor
X_test_tensor = torch.load(os.path.join(MODEL_DIR, "X_test_tensor.pt"))
input_size = X_test_tensor.shape[1]
output_size = np.load(os.path.join(MODEL_DIR, "genre_classes.npy"), allow_pickle=True).shape[0]

mlp_model = DetailedMLP(input_size=input_size, output_size=output_size)
mlp_model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "mlp_model.pth")))
mlp_model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Move model and tensor to device
mlp_model.to(device)
X_test_tensor = X_test_tensor.to(device)

# Load test data for RF and XGB
rf_X_test = pd.read_csv(os.path.join(MODEL_DIR, "rf_X_test.csv"))
xgb_X_test = pd.read_csv(os.path.join(MODEL_DIR, "xgb_X_test.csv"))

# Load label encoder
with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "rb") as f:
   label_encoder = pickle.load(f)

# === Define genre mappings ===
moods = {
   "happy": ["pop", "electronic", "folk"],
   "somber": ["folk", "avant-garde", "experimental"],
   "angry": ["rock", "hip-hop"],
   "relaxed": ["electronic", "folk"],
   "anxious": ["experimental", "avant-garde"],
   "nostalgic": ["pop", "folk"],
   "excited": ["rock", "hip-hop"]
}

activities = {
   "exercising": ["hip-hop", "rock", "electronic"],
   "reading": ["folk", "experimental"],
   "studying": ["electronic", "avant-garde", "pop"],
   "cooking": ["pop", "folk", "electronic"],
   "driving": ["rock", "pop", "electronic"]
}

# === Get user selection ===
def get_user_genres():
   print("Would you like to select by:\n1. Mood\n2. Activity")
   choice = input("Enter 1 or 2: ").strip()

   if choice == '1':
      print("Moods:", ', '.join(moods.keys()))
      mood = input("Enter your mood: ").strip().lower()
      return moods.get(mood, [])
   elif choice == '2':
      print("Activities:", ', '.join(activities.keys()))
      activity = input("Enter your activity: ").strip().lower()
      return activities.get(activity, [])
   else:
      print("Invalid input.")
      return []

# === Ensemble prediction function ===
def get_ensemble_genre_predictions(rf_X, xgb_X, X_tensor, rf_model, xgb_model, mlp_model, label_encoder):
    rf_probs = rf_model.predict_proba(rf_X)
    xgb_probs = xgb_model.predict_proba(xgb_X)
    mlp_probs = torch.softmax(mlp_model(X_tensor.float()), dim=1).detach().cpu().numpy()

    # Weighted ensemble
    ensemble_probs = 0.10 * rf_probs + 0.10 * xgb_probs + 0.80 * mlp_probs
    ensemble_preds = np.argmax(ensemble_probs, axis=1)

    # label_encoder is a numpy array of class names, so just index it
    decoded_labels = label_encoder[ensemble_preds]
    return decoded_labels

# === Suggest a track ===
def suggest_track_number(predicted_labels, target_genres):
   # Normalize to lowercase for case-insensitive matching
   target_genres = [g.lower() for g in target_genres]
   matches = [i for i, genre in enumerate(predicted_labels) if genre.lower() in target_genres]
   if not matches:
      return "No tracks found for your selected mood/activity."
   selected = random.choice(matches)
   return f"Suggested track number: track_{selected}"

# === Main program ===
def main():
   user_genres = get_user_genres()
   if not user_genres:
      print("No valid genres found for the selection.")
      return

   predicted_labels = get_ensemble_genre_predictions(
      rf_X_test, xgb_X_test, X_test_tensor, rf_model, xgb_model, mlp_model, label_encoder
   )

   result = suggest_track_number(predicted_labels, user_genres)
   print(result)

# Run the script
if __name__ == "__main__":
   main()
