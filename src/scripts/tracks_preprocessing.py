import pandas as pd
import os
from datetime import datetime

# Function to format column headers
def format_column_headers(tracks_df):
   # Flatten the multi-level column headers (combine the first and second rows)
   new_columns = []
   for col in tracks_df.columns:
      if isinstance(col, tuple):
         # Concatenate the two levels of the tuple (skip if the second level is empty)
         new_col = ' '.join(filter(None, col)).strip()
         new_columns.append(new_col)
      else:
         new_columns.append(col.strip())
   # Assign the new column names to the DataFrame
   tracks_df.columns = new_columns
   # Remove any columns with 'Unnamed:' in the column name
   tracks_df = tracks_df.loc[:, ~tracks_df.columns.str.contains('^Unnamed:')]
   # Remove the first row (which is completely empty)
   tracks_df = tracks_df.iloc[1:].reset_index(drop=True)
   # Ensure track_id is consistently int64
   # tracks_df["track_id"] = pd.to_numeric(tracks_df["track_id"], errors="coerce").astype("Int64")

   return tracks_df

# Function to convert date columns to a standard format
def clean_date_columns(tracks_df):
   # List of date-related columns to convert
   date_columns = ['album date_created', 'album date_released', 'artist active_year_begin',
                  'artist active_year_end', 'artist date_created', 'track date_created', 
                  'track date_recorded']
   
   # Convert date columns to datetime format
   for col in date_columns:
      if col in tracks_df.columns:
         tracks_df[col] = pd.to_datetime(tracks_df[col], errors='coerce').dt.strftime('%Y-%m-%d')
         # Count and print missing values for the column
         missing_count = tracks_df[col].isnull().sum()
         print(f"Column '{col}': {missing_count} missing values")
   
   # Drop columns with too many missing values
   columns_to_drop = ['artist active_year_begin', 'artist active_year_end', 'track date_recorded']
   tracks_df = tracks_df.drop(columns=columns_to_drop, errors='ignore')
   print(f"\nDropped columns: {columns_to_drop}")   
   return tracks_df

# Usage
if __name__ == "__main__":

   # Paths and folders
   base_dir = os.path.abspath(os.path.join(os.getcwd()))
   metadata_folder = os.path.join(base_dir, "data", "metadata")
   output_folder = os.path.join(base_dir, "data", "processed")

   # Load the data
   tracks_df = pd.read_csv(os.path.join(metadata_folder, "tracks.csv"), header=[0, 1], low_memory=False)
   # Format column headers
   tracks_df = format_column_headers(tracks_df)
   # Convert date columns to a standard format
   tracks_df = clean_date_columns(tracks_df)
   
   # Save the processed data to the first CSV file
   os.makedirs(output_folder, exist_ok=True)
   output_filename = "tracks_preprocessed.csv"
   output_path = os.path.join(output_folder, output_filename)
   tracks_df.to_csv(output_path, index=False)
   
   # Create the second DataFrame with specific columns
   # List of date columns that are retained
   date_columns = ['album date_created', 'album date_released', 'artist date_created', 'track date_created']
   # Create a DataFrame with selected columns: track_id, date columns, track genres
   selected_columns = ['track_id'] + date_columns + ['track genres', 'track genres_all']
   track_genre_df = tracks_df[selected_columns]
   
   # Save the selected columns to a new CSV file
   output_filename_selected = "tracks_with_genres.csv"
   output_path_selected = os.path.join(output_folder, output_filename_selected)
   track_genre_df.to_csv(output_path_selected, index=False)
   
   # Print out the file names and their content lengths
   print(f"Saved preprocessed DataFrame to {output_path}")
   print(f"Saved selected columns DataFrame to {output_path_selected}")
   print(f"Length of processed DataFrame: {len(tracks_df)}")
   print(f"Length of selected columns DataFrame: {len(track_genre_df)}")

   print(tracks_df.columns)

   print(tracks_df.head())