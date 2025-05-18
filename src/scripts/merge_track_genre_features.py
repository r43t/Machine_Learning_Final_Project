"""
import pandas as pd
import os

processed_folder = "C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/processed/"

# Load CSVs
main_df = pd.read_csv(os.path.join(processed_folder, "tracks_with_primary_genres.csv"), low_memory=False)
features_df = pd.read_csv(os.path.join(processed_folder, "features_preprocessed.csv"), low_memory=False)

# Convert track_id columns to strings and strip any whitespace
main_df['track_id'] = main_df['track_id'].astype(str).str.strip()
features_df['track_id'] = features_df['track_id'].astype(str).str.strip()

# Set 'track_id' as the index
main_df.set_index('track_id', inplace=True)
features_df.set_index('track_id', inplace=True)

# Align features_df to main_df using shared track_ids
features_df = features_df.loc[main_df.index.intersection(features_df.index)]

# Drop 'track_id' from features_df since it's already in main_df
features_df = features_df.drop(columns=['track_id'], errors='ignore')

# Concatenate side-by-side
combined_df = pd.concat([main_df.loc[features_df.index], features_df], axis=1)

# Drop rows with missing values
combined_df.dropna(inplace=True)

# Remove unwanted genres from 'primary_genre'
unwanted_genres = [
   "Jazz: Vocal", "Bluegrass", "Afrobeat", "Nerdcore", "Death-Metal", "Middle East",
   "Polka", "Interview", "Black-Metal", "Rockabilly", "Easy Listening: Vocal",
   "Asia-Far East", "N. Indian Traditional", "South Indian Traditional", "Bollywood",
   "Pacific", "Celtic", "Be-Bop", "Big Band/Swing", "British Folk", "Talk Radio",
   "North African", "Flamenco", "Thrash", "Banter", "Deep Funk", "Spoken Word",
   "Bigbeat", "Radio Theater", "Rock Opera", "Opera", "Chamber Music", "Symphony",
   "Musical Theater", "Skweee", "Western Swing", "Cumbia", "Latin", "Romany (Gypsy)",
   "Gospel", "Reggae - Dancehall", "Spanish", "Country & Western", "Wonky", "Klezmer",
   "Salsa", "Nu-Jazz", "Modern Jazz", "Turkish", "Tango", "Fado", "Christmas"
]

combined_df = combined_df[~combined_df['primary_genre'].isin(unwanted_genres)]

# Reset index to bring 'track_id' back as a column
combined_df.reset_index(inplace=True)

# Reset index to bring 'track_id' back as a column
combined_df.reset_index(inplace=True)

# Export to CSV
output_path = os.path.join(processed_folder, "track_genre_feature.csv")
combined_df.to_csv(output_path, index=False)

with open(os.path.join(processed_folder, "combined_columns.txt"), "w", encoding="utf-8") as f:
   for col in combined_df.columns:
      f.write(col + "\n")

print(f"✔ Combined dataframe saved to: {output_path}")
print("✔ Column names saved to: combined_columns.txt")

print('DONE')
"""
"""
import pandas as pd
import os

processed_folder = "C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/processed/"

# Load CSVs
main_df = pd.read_csv(os.path.join(processed_folder, "tracks_with_primary_genres.csv"), low_memory=False)
features_df = pd.read_csv(os.path.join(processed_folder, "features_preprocessed.csv"), low_memory=False)

# Convert track_id columns to strings and strip any whitespace
main_df['track_id'] = main_df['track_id'].astype(str).str.strip()
features_df['track_id'] = features_df['track_id'].astype(str).str.strip()

# Set 'track_id' as the index
main_df.set_index('track_id', inplace=True)
features_df.set_index('track_id', inplace=True)

# Align features_df to main_df using shared track_ids
features_df = features_df.loc[main_df.index.intersection(features_df.index)]

# Drop 'track_id' from features_df since it's already in main_df
features_df = features_df.drop(columns=['track_id'], errors='ignore')

# Concatenate side-by-side
combined_df = pd.concat([main_df.loc[features_df.index], features_df], axis=1)

# Drop rows with missing values
combined_df.dropna(inplace=True)

# === Keep Only Top 8 Genres ===
top_8_genres = combined_df['primary_genre'].value_counts().nlargest(8).index
combined_df = combined_df[combined_df['primary_genre'].isin(top_8_genres)]

# Reset index to bring 'track_id' back as a column
combined_df.reset_index(inplace=True)

# Export to CSV
output_path = os.path.join(processed_folder, "track_genre_feature.csv")
combined_df.to_csv(output_path, index=False)

with open(os.path.join(processed_folder, "combined_columns.txt"), "w", encoding="utf-8") as f:
    for col in combined_df.columns:
        f.write(col + "\n")

print(f"✔ Combined dataframe saved to: {output_path}")
print("✔ Column names saved to: combined_columns.txt")
print("DONE")
"""
import pandas as pd
import os

processed_folder = "C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/processed/"

# Load CSVs
main_df = pd.read_csv(os.path.join(processed_folder, "tracks_with_primary_genres.csv"), low_memory=False)
features_df = pd.read_csv(os.path.join(processed_folder, "features_preprocessed.csv"), low_memory=False)

# Convert track_id columns to strings and strip any whitespace
main_df['track_id'] = main_df['track_id'].astype(str).str.strip()
features_df['track_id'] = features_df['track_id'].astype(str).str.strip()

# Set 'track_id' as the index
main_df.set_index('track_id', inplace=True)
features_df.set_index('track_id', inplace=True)

# === Keep Only Top 8 Genres (Filter before merging) ===
top_8_genres = main_df['primary_genre'].value_counts().nlargest(8).index
main_df = main_df[main_df['primary_genre'].isin(top_8_genres)]

# Align features_df to the filtered main_df using shared track_ids
features_df = features_df.loc[main_df.index.intersection(features_df.index)]

# Drop 'track_id' from features_df (if present)
features_df = features_df.drop(columns=['track_id'], errors='ignore')

# Concatenate side-by-side
combined_df = pd.concat([main_df.loc[features_df.index], features_df], axis=1)

# Drop rows with missing values
combined_df.dropna(inplace=True)

# Reset index to bring 'track_id' back as a column
combined_df.reset_index(inplace=True)

# Export to CSV
output_path = os.path.join(processed_folder, "track_genre_feature.csv")
combined_df.to_csv(output_path, index=False)

# Save column names
with open(os.path.join(processed_folder, "combined_columns.txt"), "w", encoding="utf-8") as f:
    for col in combined_df.columns:
        f.write(col + "\n")

print(f"✔ Combined dataframe saved to: {output_path}")
print("✔ Column names saved to: combined_columns.txt")
print("DONE")