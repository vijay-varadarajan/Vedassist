import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import pickle
import os

home_dir = os.path.expanduser("~")
data = pd.read_csv(os.path.join(home_dir, 'Documents/test_devsoc/core/vedassist/ml_model/vedassistdata.csv'))

# Separate the features (X) and target (y) variables
X = data.drop(['Ayurvedic Medicine', 'Ayurvedic Medicine1', 'Ayurvedic Medicine2'], axis=1)
y = data[['Ayurvedic Medicine', 'Ayurvedic Medicine1', 'Ayurvedic Medicine2']]

# Encode categorical columns
encoder = LabelEncoder()
X['Gender'] = encoder.fit_transform(X['Gender'])
X.replace({'yes': 1, 'no': 0, 'Male': 3, 'Female': 4}, inplace=True)
print('encoded')
# Create a Random Forest classifier
classifier = RandomForestClassifier()

# Train the model
classifier.fit(X, y)
print('classifier')

# User inputs as comma-separated values
user_inputs_str = input("Enter user inputs as comma-separated values: ")
user_inputs_list = user_inputs_str.split(',')
print(user_inputs_list[:11])
print(['0']*11) 

# Make predictions
if(user_inputs_list[:11] == ['0']*11):
    print("You dont have any disease!")
else:
    predictions = classifier.predict([user_inputs_list])
    print("Predicted Ayurvedic Medicines:", predictions)
    
joblib.dump(classifier, 'model.pkl')
