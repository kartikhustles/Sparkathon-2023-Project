
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn import metrics
from flask import Flask, request, render_template
import pickle

app = Flask("__name__")

df_1=pd.read_csv("first_telc.csv")

q = ""

def clean_input(value):
        return int(value.strip())
@app.route("/", methods=['GET', 'POST'])
def loadPage():
    if request.method == 'POST':
        # Process form data and make predictions
        return predict()
    else:
        return render_template('home.html', query="")

def predict():
    
    '''
    SeniorCitizen
    MonthlyCharges
    TotalCharges
    gender
    Partner
    Dependents
    PhoneService
    MultipleLines
    InternetService
    OnlineSecurity
    OnlineBackup
    DeviceProtection
    TechSupport
    StreamingTV
    StreamingMovies
    Contract
    PaperlessBilling
    PaymentMethod
    tenure
    '''
    
    input_data={
        'SeniorCitizen': float(request.form['query1']),
        'MonthlyCharges': float(request.form['query2']),
        'TotalCharges': float(request.form['query3']),
        'gender_Female': 1 if request.form['query4'] == 'Female' else 0,
        'gender_Male': 1 if request.form['query4'] == 'Male' else 0,
        'Partner_Yes': 1 if request.form['query5'] == 'Yes' else 0,
        'Partner_No': 1 if request.form['query5'] == 'No' else 0,
        'Dependents_No': 1 if request.form['query6'] == 'No' else 0,
        'Dependents_Yes': 1 if request.form['query6'] == 'Yes' else 0,
        'PhoneService_No': 1 if request.form['query7'] == 'No' else 0,
        'PhoneService_Yes': 1 if request.form['query7'] == 'Yes' else 0,
        'MultipleLines_No': 1 if request.form['query8'] == 'No' else 0,
        'MultipleLines_No phone service': 1 if request.form['query8'] == 'No phone service' else 0,
        'MultipleLines_Yes': 1 if request.form['query8'] == 'Yes' else 0,
        'InternetService_DSL': 1 if request.form['query9'] == 'DSL' else 0,
        'InternetService_Fiber optic': 1 if request.form['query9'] == 'Fiber optic' else 0,
        'InternetService_No': 1 if request.form['query9'] == 'No' else 0,
        'OnlineSecurity_No': 1 if request.form['query10'] == 'No' else 0,
        'OnlineSecurity_No internet service': 1 if request.form['query10'] == 'No internet service' else 0,
        'OnlineSecurity_Yes': 1 if request.form['query10'] == 'Yes' else 0,
        'OnlineBackup_No': 1 if request.form['query11'] == 'No' else 0,
        'OnlineBackup_No internet service': 1 if request.form['query11'] == 'No internet service' else 0,
        'OnlineBackup_Yes': 1 if request.form['query11'] == 'Yes' else 0,
        'DeviceProtection_No': 1 if request.form['query12'] == 'No' else 0,
        'DeviceProtection_No internet service': 1 if request.form['query12'] == 'No internet service' else 0,
        'DeviceProtection_Yes': 1 if request.form['query12'] == 'Yes' else 0,
        'TechSupport_No': 1 if request.form['query13'] == 'No' else 0,
        'TechSupport_No internet service': 1 if request.form['query13'] == 'No internet service' else 0,
        'TechSupport_Yes': 1 if request.form['query13'] == 'Yes' else 0,
        'StreamingTV_No': 1 if request.form['query14'] == 'No' else 0,
        'StreamingTV_No internet service': 1 if request.form['query14'] == 'No internet service' else 0,
        'StreamingTV_Yes': 1 if request.form['query14'] == 'Yes' else 0,
        'StreamingMovies_No': 1 if request.form['query15'] == 'No' else 0,
        'StreamingMovies_No internet service': 1 if request.form['query15'] == 'No internet service' else 0,
        'StreamingMovies_Yes': 1 if request.form['query15'] == 'Yes' else 0,
        'Contract_Month-to-month': 1 if request.form['query16'] == 'Month-to-month' else 0,
        'Contract_One year': 1 if request.form['query16'] == 'One year' else 0,
        'Contract_Two year': 1 if request.form['query16'] == 'Two year' else 0,
        'PaperlessBilling_No': 1 if request.form['query17'] == 'No' else 0,
        'PaperlessBilling_Yes': 1 if request.form['query17'] == 'Yes' else 0,
        'PaymentMethod_Bank transfer (automatic)': 1 if request.form['query18'] == 'Bank transfer (automatic)' else 0,
        'PaymentMethod_Credit card (automatic)': 1 if request.form['query18'] == 'Credit card (automatic)' else 0,
        'PaymentMethod_Electronic check': 1 if request.form['query18'] == 'Electronic check' else 0,
        'PaymentMethod_Mailed check': 1 if request.form['query18'] == 'Mailed check' else 0,
        'tenure_group_1 - 12': 1 if clean_input(request.form['query19']) >= 1 and clean_input(request.form['query19']) <= 12 else 0,
        'tenure_group_13 - 24': 1 if clean_input(request.form['query19']) >= 13 and clean_input(request.form['query19']) <= 24 else 0,
        'tenure_group_25 - 36': 1 if clean_input(request.form['query19']) >= 25 and clean_input(request.form['query19']) <= 36 else 0,
        'tenure_group_37 - 48': 1 if clean_input(request.form['query19']) >= 37 and clean_input(request.form['query19']) <= 48 else 0,
        'tenure_group_49 - 60': 1 if clean_input(request.form['query19']) >= 49 and clean_input(request.form['query19']) <= 60 else 0,
        'tenure_group_61 - 72': 1 if clean_input(request.form['query19']) >= 61 and clean_input(request.form['query19']) <= 72 else 0,
    }
    
    


    model = pickle.load(open("model.sav", "rb"))
    
    # data = [[inputQuery1, inputQuery2, inputQuery3, inputQuery4, inputQuery5, inputQuery6, inputQuery7, 
            #  inputQuery8, inputQuery9, inputQuery10, inputQuery11, inputQuery12, inputQuery13, inputQuery14,
            #  inputQuery15, inputQuery16, inputQuery17, inputQuery18, inputQuery19]]
    
    # new_df = pd.DataFrame(data, columns = ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender', 
    #                                        'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
    #                                        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    #                                        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
    #                                        'PaymentMethod', 'tenure'])
    new_df_encoded = pd.DataFrame([input_data])

    new_df_encoded = pd.DataFrame([input_data])

    prediction = model.predict(new_df_encoded)
    probability = model.predict_proba(new_df_encoded)[:, 1]

    if prediction == 1:
        output1 = "This customer is likely to be churned!!"
    else:
        output1 = "This customer is likely to continue!!"
        
    output2 = "Probability: {:.2f}%".format(probability[0] * 100)

    return render_template('home.html', output1=output1, output2=output2, **input_data)

if __name__ == "__main__":
    app.run(debug=True)

