import pandas as pd

# Load datasets
tracks_df = pd.read_csv("C:/Users/retae/GitHub/Machine_Learning_Final_Project/data/processed/tracks_preprocessed.csv", low_memory=False)
features_df = pd.read_csv("C:/Users/retae/GitHub/Machine_Learning_Final_Project/data/processed/features_preprocessed.csv", low_memory=False)

# Ensure column names are stripped of spaces
tracks_df.rename(columns=lambda x: x.strip(), inplace=True)
features_df.rename(columns=lambda x: x.strip(), inplace=True)

# Drop 'track_id' column from features_df (since it's already in tracks_df)
if 'track_id' in features_df.columns:
    features_df = features_df.drop(columns=['track_id'])

# Concatenate dataframes side by side
merged_df = pd.concat([tracks_df, features_df], axis=1)

# Save merged dataset
output_path = "C:/Users/retae/GitHub/Machine_Learning_Final_Project/data/processed/merged_tracks_features.csv"
merged_df.to_csv(output_path, index=False)

print(f"Merged DataFrame saved successfully with {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.")

# Display the first few rows of the merged dataframe
print(merged_df.head())

print(merged_df.columns)