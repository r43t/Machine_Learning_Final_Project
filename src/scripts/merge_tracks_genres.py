import pandas as pd
import os
import ast

# Paths to folders
base_dir = os.path.abspath(os.path.join(os.getcwd()))
metadata_folder = os.path.join(base_dir, "data", "metadata")
processed_folder = os.path.join(base_dir, "data", "processed")

# Load the data
tracks_df = pd.read_csv(os.path.join(processed_folder, "tracks_preprocessed.csv"), header=0, low_memory=False)
genres_df = pd.read_csv(os.path.join(metadata_folder, "genres.csv"), low_memory=False)

# Ensure the genre_id and title columns exist in genres_df
if 'genre_id' not in genres_df.columns or 'title' not in genres_df.columns:
    raise KeyError("'genre_id' or 'title' column is missing in genres_df")

def extract_first_genre(x):
    try:
        lst = ast.literal_eval(x)
        return lst[0] if isinstance(lst, list) and len(lst) > 0 else None
    except Exception:
        return None

# Apply to the column
tracks_df['track genres'] = tracks_df['track genres'].apply(extract_first_genre)


# Merge the DataFrames on track genres and genre_id, including the 'title' column
merged_df = pd.merge(tracks_df, genres_df[['genre_id', 'title']], left_on='track genres', right_on='genre_id', how='inner')

# Print the new columns after merging
print("New columns in the merged DataFrame:")
print(merged_df.columns)

# Export the merged DataFrame to a new CSV
merged_df.to_csv(os.path.join(processed_folder, "tracks_preprocessed.csv"), index=False)