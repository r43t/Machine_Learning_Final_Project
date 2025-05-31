import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os

# Paths
base_dir = os.path.abspath(os.path.join(os.getcwd()))
file_path = os.path.join(base_dir, "data", "processed", "track_genre_feature.csv")
output_path = os.path.join(base_dir, "data", "processed", "final.csv")

# Load combined data
df = pd.read_csv(file_path)

# Keep track_id for later
track_ids = df['track_id']

# Separate labels and features
y = df['primary_genre']
X = df.drop(columns=[
    'primary_genre',
    'album date_created', 'album date_released', 
    'artist date_created', 'track date_created', 
    'track genres_all'
], errors='ignore')  # keep 'track_id'

# Optional: Log transform skewed features
# skewed_feats = X.select_dtypes(include=[np.number]).skew().sort_values(ascending=False)
# skewed_cols = skewed_feats[skewed_feats > 1.0].index
# X[skewed_cols] = np.log1p(X[skewed_cols])

# Standardize numerical features (excluding 'track_id')
numerical_cols = X.select_dtypes(include=[np.number]).columns
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X[numerical_cols])

# Feature Selection: Keep top 50 features using ANOVA F-test
k = min(50, X_scaled.shape[1])
selector = SelectKBest(score_func=f_classif, k=k)
X_selected = selector.fit_transform(X_scaled, y)

# PCA: Retain 95% of variance
pca = PCA(n_components=0.95, random_state=42)
X_pca = pca.fit_transform(X_selected)

# Create DataFrame for reduced features
X_pca_df = pd.DataFrame(X_pca, columns=[f'pc_{i+1}' for i in range(X_pca.shape[1])])
X_pca_df.insert(0, 'track_id', track_ids.values)
X_pca_df['primary_genre'] = y.values

# Save final DataFrame
os.makedirs(os.path.dirname(output_path), exist_ok=True)
X_pca_df.to_csv(output_path, index=False)
print(f"✅ Saved final preprocessed dataset with track_id to: {output_path}")

# Train-test split (optional, for modeling later)
X_train, X_test, y_train, y_test = train_test_split(
    X_pca, y, test_size=0.3, stratify=y, random_state=42
)

# Summary
print(f"\n📊 Summary:")
print(f"Original features: {X.shape}")
print(f"After feature selection: {X_selected.shape}")
print(f"After PCA: {X_pca.shape}")
print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

# Plot explained variance
plt.figure(figsize=(8, 4))
plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Explained Variance')
plt.grid(True)
plt.tight_layout()
plt.show()