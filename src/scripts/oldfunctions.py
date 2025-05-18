"""
# Main function to load data, apply formatting, and save the result
def preprocess_and_save(metadata_folder, output_folder):
   # Load tracks.csv with header=0 and header=1 to combine the first two rows as column names
   tracks_path = os.path.join(metadata_folder, "tracks.csv")
   
   # Read the file with two header rows (header=[0, 1])
   tracks_df = pd.read_csv(tracks_path, header=[0, 1], low_memory=False)

   # Step 1: Format column headers
   tracks_df = format_column_headers(tracks_df)
   
   # Step 2: Convert date columns
   tracks_df = convert_dates_to_standard(tracks_df)

   # Drop columns with mostly empty values (you can adjust the threshold)
   tracks_df = tracks_df.dropna(axis=1, thresh=int(0.5 * len(tracks_df)))

   # Ensure the output folder exists
   os.makedirs(output_folder, exist_ok=True)

   # Output file
   output_filename = "tracks_preprocessed.csv"
   output_path = os.path.join(output_folder, output_filename)

   # Save the DataFrame to a new CSV file
   tracks_df.to_csv(output_path, index=False)

   # Print out the new column names
   print("Combined column names:")
   for col in tracks_df.columns:
      print(col)

   # Print confirmation of where the file was saved
   print(f"Saved preprocessed DataFrame to {output_path}")
"""