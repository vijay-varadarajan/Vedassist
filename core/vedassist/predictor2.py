import pandas as pd
import pickle
import joblib
import os


downloads_dir = os.path.join("", "C:/Users/varad/Documents/Vedassist/core/vedassist/ml_model/model2.pkl")
regressor = joblib.load(downloads_dir)
object_cols = ['Herb', 'Allopathic Medicine', 'Age', 'Gender', 'Weight', 'Dosage', 'Duration']


def format_input(user_input):
    user_input = user_input.split(',')
    user_data = pd.DataFrame({
        "Herb": [user_input[0]],
        "Allopathic Medicine": [user_input[1]],
        "Age": [user_input[2]],
        "Gender": [user_input[3]],
        "Weight": [user_input[4]],
        "Dosage": [user_input[5]],
        "Duration": [user_input[6]],
    })
    print("dataframed")
    print(user_data)
    
    with open("C:/Users/varad/Documents/Vedassist/core/vedassist/ml_model/codes.pkl", 'rb') as file:
        label_codes = pickle.load(file)
    
        
    print(user_data)
    return user_data

def model_predict2(user_input):
    
    print(user_input, "this is user input")
    user_data = format_input(user_input)    

    prediction = regressor.predict(user_data)
    print("prediction: ", prediction)
    return prediction
