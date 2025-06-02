# Music Genre Classification and Recommendation System

This repository contains the code and resources for a machine learning project that classifies music tracks by genre and provides a mood/activity-based music recommendation system. The project uses the Free Music Archive (FMA) small dataset and applies multiple ML models to classify tracks based on audio features.

**Note: Dataset folders containing the tracks and CSV files are not in this repository because they are too large and thus require Git LFS for upload and commits. I did not want to pay for this subscription.**

## Project Overview

The goal of this project is to classify music tracks into genres using audio feature extraction and machine learning, and then leverage the classification results to recommend songs based on user-selected moods or activities.

### Dataset

- **FMA Small Dataset:** A curated subset of the Free Music Archive dataset, consisting of 8,000+ tracks across various genres.
- The dataset was cleaned and preprocessed before feature extraction.

### Features Used

- **MFCC (Mel Frequency Cepstral Coefficients)**
- **Spectral Contrast**
- **Chroma Features**

These features were extracted from the audio tracks to represent important aspects of the music for classification.

### Machine Learning Models

Three different models were trained and evaluated for genre classification:

1. **Random Forest Classifier**
2. **XGBoost Classifier**
3. **Multilayer Perceptron (MLP) Neural Network**

An **ensemble model** was also created by combining the predictions of these three classifiers with varied weights to improve overall accuracy.

### Recommendation System

- Built on top of the ensemble classification results.
- Offers users a choice among **7 different moods** and **5 different activities**.
- Based on the user's selection, the system recommends a random song from the genre that best aligns with the chosen mood or activity.

## Repository Structure

- `data/` — Preprocessed dataset and features  
- `notebooks/` — Jupyter notebooks for data cleaning, feature extraction, and model training  
- `models/` — Saved trained models and ensemble weights  
- `src/` — Python scripts for training models, running inference, and the recommendation system  
- `README.md` — This file  

## How to Use

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

3. **Run Preprocessing and Feature Extraction**

    Execute scripts/notebooks in the order specified in the notebooks or src folders to preprocess data and extract features.

4. **Train Models**

    Run the training scripts to train the Random Forest, XGBoost, and MLP models.

5. **Run the Ensemble and Recommendation System**

    Use the provided script to load the ensemble model and interact with the recommendation system by selecting moods or activities.

## Technologies Used

- Python 3.10
- Scikit-Learn
- XGBoost 
- Pytorch
- Numpy
- Pandas
- Matplotlib

## Future Work

- Incorporate more advanced deep learning models for improved classification.
- Expand recommendation system to use user feedback and personalization.
- Support additional datasets and multilingual music tracks.

## License

This project is licensed under the MIT license.
