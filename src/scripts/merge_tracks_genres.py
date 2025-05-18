import pandas as pd
import os

# Input and Output folder locations
metadata_folder = "C:/Users/retae/GitHub/Machine_Learning_Final_Project/data/metadata/"
processed_folder = "C:/Users/retae/GitHub/Machine_Learning_Final_Project/data/processed/"

# Load the data
tracks_df = pd.read_csv(os.path.join(processed_folder, "tracks_preprocessed.csv"), header=[0, 1], low_memory=False)
genres_df = pd.read_csv(os.path.join(processed_folder, "genres.csv"), low_memory=False)

# Flatten the MultiIndex columns in both DataFrames
tracks_df.columns = [' '.join(col).strip() for col in tracks_df.columns.values]
genres_df.columns = [' '.join(col).strip() for col in genres_df.columns.values]

# Ensure the genre_id and title columns exist in genres_df
if 'genre_id' not in genres_df.columns or 'title' not in genres_df.columns:
    raise KeyError("'genre_id' or 'title' column is missing in genres_df")

# Merge the DataFrames on track genres and genre_id, including the 'title' column
merged_df = pd.merge(tracks_df, genres_df[['genre_id', 'title']], left_on='track genres', right_on='genre_id', how='inner')

# Print the new columns after merging
print("New columns in the merged DataFrame:")
print(merged_df.columns)

# Export the merged DataFrame to a new CSV
merged_df.to_csv('combined_tracks_genres.csv', index=False)

"""
import pandas as pd
import os

# Input and Output folder locations
metadata_folder = "C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/metadata/"
processed_folder = "C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/processed/"

# Load the data
tracks_df = pd.read_csv(os.path.join(processed_folder, "tracks_preprocessed.csv"), header=[0, 1], low_memory=False)
genres_df = pd.read_csv(os.path.join(metadata_folder, "genres.csv"), header=[0, 1], low_memory=False)

# Flatten the MultiIndex columns in both DataFrames
tracks_df.columns = [' '.join(col).strip() for col in tracks_df.columns.values]
genres_df.columns = [' '.join(col).strip() for col in genres_df.columns.values]

# Merge the DataFrames on track_id and genre_id
merged_df = pd.merge(tracks_df, genres_df, left_on='track genres', right_on='genre_id', how='inner')

# Print the new columns after merging
print("New columns in the merged DataFrame:")
print(merged_df.columns)

# Export the merged DataFrame to a new CSV
merged_df.to_csv('combined_tracks_genres.csv', index=False)
"""