import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import datetime

# Load the preprocessed dataset
def load_data(file_path):
    cars_data = pd.read_csv(file_path)
    return cars_data

# Load the preprocessed data
file_path = 'original_dataset.csv'
cars_data = load_data(file_path)

# Remove duplicate rows
cars_data = cars_data.drop_duplicates()

# Rename 'Car documents' column
cars_data.rename(columns={'Car documents': 'Car Documents'}, inplace=True)

# Calculate age of each car
current_year = datetime.datetime.now().year
cars_data['Age'] = current_year - cars_data['Year']

# Drop the unnecessary columns
cars_data = cars_data.drop(columns=['Ad ID', 'Images URL\'s', 'Car Profile'])

# Shuffle the data
cars_data = cars_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Split the 'Car Features' column and explode it to create a Series
car_features_series = cars_data['Car Features'].str.split(', ').explode()

# Get the value counts of each feature
feature_counts = car_features_series.value_counts()

# Extract the top 5 most common features
top_5_features = feature_counts.head(5).index

# List of most existed features
most_existed_features = top_5_features

# Create columns for each feature and initialize with zeros
for feature in most_existed_features:
    cars_data[feature] = 0

# Iterate over each record and update the new columns accordingly
for index, row in cars_data.iterrows():
    features = row['Car Features'].split(', ')
    for feature in features:
        if feature in most_existed_features:
            cars_data.at[index, feature] = 1

# Drop the original 'Car Features' column
cars_data.drop(columns=['Car Features'], inplace=True)

# Select the features relevant for recommendation
features = cars_data[['Make', 'Model', 'Age', "KM's driven", 'Price', 'Fuel', 'Car Documents', 'Assembly', 'Transmission', 'Air Conditioning', 'AM/FM Radio', 'Power Steering', 'Front Speakers', 'Power Locks']]

# Perform one-hot encoding for categorical features
categorical_cols = ['Make', 'Model', 'Fuel', 'Car Documents', 'Assembly', 'Transmission']
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(features[categorical_cols])
encoded_features_array = encoded_features.toarray()

# Scale numerical features
numerical_cols = ['Age', "KM's driven", 'Price']
scaler = StandardScaler()
scaled_numerical_features = scaler.fit_transform(features[numerical_cols])

# Combine encoded categorical features and scaled numerical features
all_features = np.concatenate((encoded_features_array, scaled_numerical_features, features[['Air Conditioning', 'AM/FM Radio', 'Power Steering', 'Front Speakers', 'Power Locks']].values), axis=1)

# Compute cosine similarity matrix
similarity_matrix = cosine_similarity(all_features)

# Set a limit for the returned recommended cars
limit = 5

def get_top_similar_cars_user_input(user_input, similarity_matrix=similarity_matrix, limit=limit):
    # Encode user input
    user_encoded = encoder.transform([[user_input['Make'], user_input['Model'], user_input['Fuel'], user_input['Car Documents'], user_input['Assembly'], user_input['Transmission']]])
    # Scale numerical features of user input
    user_numerical_features = scaler.transform([[user_input['Age'], user_input["KM's driven"], user_input['Price']]])
    # Combine encoded categorical features and scaled numerical features
    user_input_features = np.concatenate((user_encoded.toarray(), user_numerical_features, np.array([[user_input[feature] for feature in ['Air Conditioning', 'AM/FM Radio', 'Power Steering', 'Front Speakers', 'Power Locks']]])), axis=1)
    # Compute similarity scores between user input and all cars
    similarity_scores = cosine_similarity(user_input_features, all_features)
    
    # Get the indices of similar cars
    similar_car_indices = similarity_scores.argsort()[0][::-1]
    
    # Filter the results based on the selected make and model
    similar_cars = cars_data.loc[similar_car_indices]
    similar_cars = similar_cars[(similar_cars['Make'] == user_input['Make']) & (similar_cars['Model'] == user_input['Model'])][:limit]
    
    # Convert similar cars to a list of dictionaries
    recommendations = []
    for index, row in similar_cars.iterrows():
        car_info = {
            'Make': row['Make'],
            'Model': row['Model'],
            'Year': row['Year'],
            'Price': row['Price'],
            'Description': row['Description']
        }
        recommendations.append(car_info)
    
    return recommendations
