import pandas as pd
import ast
import os

# Paths
base_dir = os.path.abspath(os.path.join(os.getcwd()))
processed_folder = os.path.join(base_dir, "data", "processed")

# 1. Load the CSV
genres_df = pd.read_csv(os.path.join(processed_folder, "tracks_with_genres.csv"), low_memory=False)

# 2. Define the genre ID to name mapping
genre_map = {
   1: 'Avant-Garde', 2: 'International', 3: 'Blues', 4: 'Jazz', 5: 'Classical',
   6: 'Novelty', 7: 'Comedy', 8: 'Old-Time / Historic', 9: 'Country', 10: 'Pop',
   11: 'Disco', 12: 'Rock', 13: 'Easy Listening', 14: 'Soul-RnB', 15: 'Electronic',
   16: 'Sound Effects', 17: 'Folk', 18: 'Soundtrack', 19: 'Funk', 20: 'Spoken',
   21: 'Hip-Hop', 22: 'Audio Collage', 25: 'Punk', 26: 'Post-Rock', 27: 'Lo-Fi',
   30: 'Field Recordings', 31: 'Metal', 32: 'Noise', 33: 'Psych-Folk', 36: 'Krautrock',
   37: 'Jazz: Vocal', 38: 'Experimental', 41: 'Electroacoustic', 42: 'Ambient Electronic',
   43: 'Radio Art', 45: 'Loud-Rock', 46: 'Latin America', 47: 'Drone', 49: 'Free-Folk',
   53: 'Noise-Rock', 58: 'Psych-Rock', 63: 'Bluegrass', 64: 'Electro-Punk', 65: 'Radio',
   66: 'Indie-Rock', 70: 'Industrial', 71: 'No Wave', 74: 'Free-Jazz', 76: 'Experimental Pop',
   77: 'French', 79: 'Reggae - Dub', 81: 'Afrobeat', 83: 'Nerdcore', 85: 'Garage',
   86: 'Indian', 88: 'New Wave', 89: 'Post-Punk', 90: 'Sludge', 92: 'African',
   94: 'Freak-Folk', 97: 'Jazz: Out', 98: 'Progressive', 100: 'Alternative Hip-Hop',
   101: 'Death-Metal', 102: 'Middle East', 103: 'Singer-Songwriter', 107: 'Ambient',
   109: 'Hardcore', 111: 'Power-Pop', 113: 'Space-Rock', 117: 'Polka', 118: 'Balkan',
   125: 'Unclassifiable', 130: 'Europe', 137: 'Americana', 138: 'Spoken Weird',
   166: 'Interview', 167: 'Black-Metal', 169: 'Rockabilly', 170: 'Easy Listening: Vocal',
   171: 'Brazilian', 172: 'Asia-Far East', 173: 'N. Indian Traditional',
   174: 'South Indian Traditional', 175: 'Bollywood', 176: 'Pacific', 177: 'Celtic',
   178: 'Be-Bop', 179: 'Big Band/Swing', 180: 'British Folk', 181: 'Techno', 182: 'House',
   183: 'Glitch', 184: 'Minimal Electronic', 185: 'Breakcore - Hard', 186: 'Sound Poetry',
   187: '20th Century Classical', 188: 'Poetry', 189: 'Talk Radio', 214: 'North African',
   224: 'Sound Collage', 232: 'Flamenco', 236: 'IDM', 240: 'Chiptune', 247: 'Musique Concrete',
   250: 'Improv', 267: 'New Age', 286: 'Trip-Hop', 296: 'Dance', 297: 'Chip Music',
   311: 'Lounge', 314: 'Goth', 322: 'Composed Music', 337: 'Drum & Bass', 359: 'Shoegaze',
   360: 'Kid-Friendly', 361: 'Thrash', 362: 'Synth Pop', 374: 'Banter', 377: 'Deep Funk',
   378: 'Spoken Word', 400: 'Chill-out', 401: 'Bigbeat', 404: 'Surf', 428: 'Radio Theater',
   439: 'Grindcore', 440: 'Rock Opera', 441: 'Opera', 442: 'Chamber Music',
   443: 'Choral Music', 444: 'Symphony', 456: 'Minimalism', 465: 'Musical Theater',
   468: 'Dubstep', 491: 'Skweee', 493: 'Western Swing', 495: 'Downtempo', 502: 'Cumbia',
   504: 'Latin', 514: 'Sound Art', 524: 'Romany (Gypsy)', 538: 'Compilation',
   539: 'Rap', 542: 'Breakbeat', 567: 'Gospel', 580: 'Abstract Hip-Hop',
   602: 'Reggae - Dancehall', 619: 'Spanish', 651: 'Country & Western',
   659: 'Contemporary Classical', 693: 'Wonky', 695: 'Jungle', 741: 'Klezmer',
   763: 'Holiday', 808: 'Salsa', 810: 'Nu-Jazz', 811: 'Hip-Hop Beats',
   906: 'Modern Jazz', 1032: 'Turkish', 1060: 'Tango', 1156: 'Fado',
   1193: 'Christmas', 1235: 'Instrumental'
}

# 3. Clean and convert 'track genre' field
def extract_primary_genre(genre_list_str):
   try:
      genre_ids = ast.literal_eval(genre_list_str)
      if isinstance(genre_ids, list) and genre_ids:
         return genre_map.get(genre_ids[0], "Unknown")
   except:
      return "Unknown"

genres_df["primary_genre"] = genres_df["track genres"].apply(extract_primary_genre)

# 4. Drop the old column and/or reorder if needed
genres_df.drop(columns=["track genres"], inplace=True)

# 5. Save the updated DataFrame
output_path = processed_folder + "tracks_with_primary_genres.csv"
genres_df.to_csv(output_path, index=False)
print("✅ Output saved to 'tracks_with_primary_genres.csv'")