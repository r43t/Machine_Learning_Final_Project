import pandas as pd
import os

# Paths
base_dir = os.path.abspath(os.path.join(os.getcwd()))
tracks_path = os.path.join(base_dir, "data", "processed", "tracks_preprocessed.csv")
features_path = os.path.join(base_dir, "data", "processed", "features_preprocessed.csv")
output_path = os.path.join(base_dir, "data", "processed", "merged_tracks_features.csv")

# Load datasets
tracks_df = pd.read_csv(tracks_path, low_memory=False)
features_df = pd.read_csv(features_path, low_memory=False)

# Ensure column names are stripped of spaces
tracks_df.rename(columns=lambda x: x.strip(), inplace=True)
features_df.rename(columns=lambda x: x.strip(), inplace=True)

# Drop 'track_id' column from features_df (since it's already in tracks_df)
if 'track_id' in features_df.columns:
    features_df = features_df.drop(columns=['track_id'])

# Concatenate dataframes side by side
merged_df = pd.concat([tracks_df, features_df], axis=1)

# Save merged dataset
merged_df.to_csv(output_path, index=False)

print(f"Merged DataFrame saved successfully with {merged_df.shape[0]} rows and {merged_df.shape[1]} columns.")

# Display the first few rows of the merged dataframe
print(merged_df.head())

print(merged_df.columns)