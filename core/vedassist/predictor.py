import pandas as pd
import pickle
import joblib
import os

downloads_dir = os.path.join("", "C:/Users/varad/Documents/test_devsoc/core/vedassist/ml_model/model.pkl")
classifier = joblib.load(downloads_dir)

def model_predict(user_input):
    # sourcery skip: inline-immediately-returned-variable
    user_input = user_input.split(',')
    user_data = pd.DataFrame({ 'Cold': [user_input[0]],
            'Eyepain' :[user_input[1]],
            'Fever': [user_input[2]],
            'Headache': [user_input[3]],
            'Stomachache': [user_input[4]],
            'Dizziness': [user_input[5]],
            'Vomiting': [user_input[6]],
            'Chestpain': [user_input[7]],
            'Jointpain': [user_input[8]],
            'Loosemotion': [user_input[9]],
            'Throatinfection':[user_input[10]],
            'Age': [user_input[11]],
            'Gender': [user_input[12]],
            'Weight': [user_input[13]],
             })
    prediction = classifier.predict(user_data)
    return prediction
    