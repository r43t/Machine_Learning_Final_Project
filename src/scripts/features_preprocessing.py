"""
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt, seaborn as sns
import IPython.display as ipd
import os

def rename_fma_features(features):
    df_features_name = features.iloc[:2,1:]
    new_feature_name = ['track_id']
    for i in range(len(df_features_name.columns)):
        feat = df_features_name.iloc[:,i]
        feat_name = feat.name.split('.')[0]
        stat = feat[0]
        num = feat[1]
        name = feat_name+'_'+num+'_'+stat
        new_feature_name.append(name)
    return_df = features.iloc[3:,:].reset_index(drop=True)
    return_df.columns = new_feature_name
    return return_df

# Usage
raw_features = pd.read_csv('C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/metadata/features.csv', low_memory=False)
features = rename_fma_features(raw_features)
features = features.apply(pd.to_numeric)
# Print to check
print(raw_features.head())

# Define the path where the file will be saved
output_path = 'C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/processed/features_preprocessed.csv'
# Ensure the folder exists before saving
os.makedirs(os.path.dirname(output_path), exist_ok=True)
# Save the processed dataframe to a .csv file
features.to_csv(output_path, index=False)
print(f"Preprocessed dataframe saved to {output_path}")

track_id_list = features['track_id'].tolist()

print(len(track_id_list))

print(features.columns)

print(features.head())
"""
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt, seaborn as sns
import IPython.display as ipd
import os

def rename_fma_features(features):
    df_features_name = features.iloc[:2, 1:]
    new_feature_names = ['track_id']
    name_map = []  # Keep track of (base_name, original_column)

    for i in range(len(df_features_name.columns)):
        feat = df_features_name.iloc[:, i]
        feat_name = feat.name.split('.')[0]
        stat = feat[0]
        num = feat[1]
        full_name = feat_name + '_' + num + '_' + stat
        new_feature_names.append(full_name)
        name_map.append((feat_name, num, stat, full_name))

    return_df = features.iloc[3:, :].reset_index(drop=True)
    return_df.columns = new_feature_names
    return return_df, name_map

def group_features_by_statistic(df, name_map):
    grouped = {}  # key: (feat_name, stat), value: list of columns
    ungrouped = []  # For features that don’t have siblings to group with

    for feat_name, num, stat, full_name in name_map:
        key = (feat_name, stat)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(full_name)

    grouped_features = pd.DataFrame()
    grouped_features['track_id'] = df['track_id']

    for (feat_name, stat), columns in grouped.items():
        if len(columns) == 1:
            # Only one feature with this stat, keep as is
            grouped_features[columns[0]] = df[columns[0]]
        else:
            # Aggregate (e.g., mean) across matching features
            new_col_name = f'{feat_name}_{stat}'
            grouped_features[new_col_name] = df[columns].mean(axis=1)

    return grouped_features

# Load raw features
raw_features = pd.read_csv(
    'C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/metadata/features.csv', 
    low_memory=False
)

# Rename and parse features
features, name_map = rename_fma_features(raw_features)
features = features.apply(pd.to_numeric)

# Group features by summary statistic
features_grouped = group_features_by_statistic(features, name_map)

# Save processed DataFrame
output_path = 'C:/Users/retae/GitHub/Machine-Learning-Final-Project/data/processed/features_preprocessed.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
features_grouped.to_csv(output_path, index=False)

print(f"Preprocessed dataframe saved to {output_path}")
print(f"Total number of tracks: {len(features_grouped)}")
print(f"New columns: {features_grouped.columns.tolist()}")
print(features_grouped.head())
