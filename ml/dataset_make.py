import pandas as pd
import os

def initialize_dataset(file_path="dataset.csv"):
    # Define column names: 7 feature columns + 4 class columns
    feature_columns = [f"feature_{i+1}" for i in range(7)]
    class_columns = ["class"]
    columns = feature_columns + class_columns

    # If the file doesn't exist, create it with headers
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)

def add_instance(features, one_hot_class, file_path="dataset.csv"):
    # Validate input dimensions
    if len(features) != 7:
        raise ValueError("Expected 7 features.")

    # Create a single-row DataFrame for the new instance
    one_hot_classt = [one_hot_class]
    instance = features + one_hot_classt
    df = pd.DataFrame([instance])

    # Append to the CSV file without headers
    df.to_csv(file_path, mode='a', header=False, index=False)

initialize_dataset();

x = [3.4,5.3,54.5,2.0,2.4,5.9,12.2]
y = 0

add_instance(x,y)

x = [xi/2 for xi in x]
y = 3

add_instance(x,y)

df = pd.read_csv('dataset.csv')

# Split into data features and target features
data_features = df.iloc[:, :7]  # First 7 columns
target_features = df.iloc[:, 7:]  # Last 4 columns

print("data: \n", data_features.to_numpy())
print("\ntarget: \n", target_features)
