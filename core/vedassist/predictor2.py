import pandas as pd
import pickle
import joblib
import os

downloads_dir = os.path.join("", "C:/Users/varad/Documents/Vedassist/core/vedassist/ml_model/model2.pkl")
regressor = joblib.load(downloads_dir)

def model_predict2(user_input):
    # sourcery skip: inline-immediately-returned-variable
    user_input = user_input.split(',')
    user_data = pd.DataFrame({
        'Herb': [user_input[0]],
        'Allopathic Medicine': [user_input[1]],
        'Age': [user_input[2]],
        'Gender': [user_input[3]],
        'Weight': [user_input[4]],
        'Dosage': [user_input[5]],
        'Duration': [user_input[6]],
    })
    prediction = regressor.predict(user_data)
    return prediction
