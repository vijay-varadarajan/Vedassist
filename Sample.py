import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import pickle
import os

# Load the dataset
data = pd.read_csv('vedassist_2.csv')

# Replace missing values with the most frequent value in each column
data = data.fillna(data.mode().iloc[0])

# Prepare the data for training
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Encode the first two columns and gender column
label_encoder = LabelEncoder()
X['Herb'] = label_encoder.fit_transform(X['Herb'])
X['Allopathic Medicine'] = label_encoder.fit_transform(X['Allopathic Medicine'])
X['Gender'] = label_encoder.fit_transform(X['Gender'])

# Encode the Adverse Effect column
y_encoded = label_encoder.fit_transform(y)

# Convert categorical variables to numerical using one-hot encoding
X = pd.get_dummies(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Create and train the logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy and r-squared score
accuracy = accuracy_score(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Accuracy:", accuracy*100,"%")
print("R-squared Score:", r2)

joblib.dump(model, 'model2.pkl')
print("dumped")

# Get user input as a comma-separated string
user_input = input("Enter comma-separated values for Herb, Allopathic Medicine, Age, Gender, Weight, Dosage, Duration: ")

# Split the user input into a list of values
user_input = user_input.split(',')

# Convert user input to a dataframe
user_df = pd.DataFrame([user_input], columns=X.columns)

# Replace missing values in user input with the most frequent value in each column
user_df = user_df.fillna(user_df.mode().iloc[0])

# Encode the first two columns and gender column using the label_encoder from training
user_df['Herb'] = user_df['Herb'].apply(lambda x: label_encoder.transform([x])[0] if x in label_encoder.classes_ else -1)
user_df['Allopathic Medicine'] = user_df['Allopathic Medicine'].apply(lambda x: label_encoder.transform([x])[0] if x in label_encoder.classes_ else -1)
user_df['Gender'] = user_df['Gender'].apply(lambda x: label_encoder.transform([x])[0] if x in label_encoder.classes_ else -1)

# Make prediction based on user input
prediction_encoded = model.predict(user_df)
prediction = label_encoder.inverse_transform(prediction_encoded)

print("Predicted Adverse Effect:", prediction[0])
