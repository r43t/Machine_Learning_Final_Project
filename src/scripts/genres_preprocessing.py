import pandas as pd
import os

def missing_values(genres_df):
    return genres_df.isnull().sum()

def map_genre_ids_to_titles(genres_df):
    """
    Maps genre_id to title using the genres_df DataFrame.
    Assumes that 'genre_id' and 'title' columns are present in the DataFrame.
    """
    # Ensure that 'genre_id' and 'title' are present as columns
    if 'genre_id' not in genres_df.columns or 'title' not in genres_df.columns:
        raise KeyError("'genre_id' or 'title' column is missing")

    # Access the genre_id column
    genre_id_column = genres_df['genre_id']
    
    # Access the title column
    title_column = genres_df['title']

    # Create a dictionary mapping genre_id to title
    genre_mapping = dict(zip(genre_id_column, title_column))

    return genre_mapping

# Usage
if __name__ == "__main__":
    # Paths and folders
    base_dir = os.path.abspath(os.path.join(os.getcwd()))
    metadata_folder = os.path.join(base_dir, "data", "metadata")
    processed_folder = os.path.join(base_dir, "data", "processed")

    # Load the data (no multiindex issue anymore)
    genres_df = pd.read_csv(os.path.join(processed_folder, "genres.csv"), low_memory=False)

    # Step 1: Check for missing values
    missing = missing_values(genres_df)
    print("Missing values in the DataFrame:", missing)

    # Step 2: Call the genre mapping function
    genre_mapping = map_genre_ids_to_titles(genres_df)
    print("Genre ID to Title Mapping: ", genre_mapping)

    print(genres_df.head())

        # Step 3: Print genres with fewer than 50 tracks
    if '#tracks' in genres_df.columns:
        low_track_genres = genres_df[genres_df['#tracks'] < 300]
        print("\nGenres with fewer than 300 tracks:")
        print(low_track_genres[['title', '#tracks']])
    else:
        print("\nColumn '#tracks' not found in DataFrame.")