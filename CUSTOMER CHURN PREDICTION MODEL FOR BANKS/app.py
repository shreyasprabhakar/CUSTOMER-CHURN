from flask import Flask, render_template, request,redirect, url_for
import requests
import pickle
import numpy as np
import sklearn
import matplotlib
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))

users = {
    "user1": {
        "password": "password1"
    },
    "user2": {
        "password": "password2"
    }
}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact')
def buy():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # Valid credentials, redirect to predictions page
            return redirect(url_for('predictions'))
        else:
            # Invalid credentials, show login page with error message
            return render_template('login.html', error='Invalid username or password')
    # GET request, show login page
    return render_template('login.html', error='')

standard_to = StandardScaler()
@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    if request.method == 'POST':
        # Handle form submission for predictions here
        # Example: Get form data
        credit_score = request.form['CreditScore']
        Gender_Male = request.form['Gender_Male']
        age = request.form['Age']
        tenure = request.form['Tenure']
        balance = request.form['Balance']
        num_of_products = request.form['NumOfProducts']
        has_cr_card = request.form['HasCrCard']
        is_active_member = request.form['IsActiveMember']
        estimated_salary = request.form['EstimatedSalary']
        # Here, you can process the form data, perform prediction, etc.
        Geography_Mumbai = request.form['Geography_Mumbai']
        if(Geography_Mumbai == 'Mumbai'):
            Geography_Mumbai = 1
            Geography_Chennai= 0
            Geography_Delhi = 0
                
        elif(Geography_Mumbai == 'Chennai'):
            Geography_Mumbai = 0
            Geography_Chennai= 1
            Geography_Delhi = 0
        
        else:
            Geography_Mumbai = 0
            Geography_Chennai= 0
            Geography_Delhi = 1
        Gender_Male = request.form['Gender_Male']
        if(Gender_Male == 'Male'):
            Gender_Male = 1
            Gender_Female = 0
        else:
            Gender_Male = 0
            Gender_Female = 1
        prediction = model.predict([[credit_score,age,tenure,balance,num_of_products,has_cr_card,is_active_member,estimated_salary,Geography_Mumbai,Geography_Chennai,Gender_Male]])
        if prediction==1:
             return render_template('prediction.html',prediction_text="The Customer will leave the bank")
        elif prediction==0:
            return render_template('prediction.html',prediction_text="The Customer will not leave the bank")
        else:
             return render_template('prediction.html',prediction_text = "Invalid")
        
    # GET request, show predictions page
    return render_template('prediction.html', prediction_result="prediction_text")


                
if __name__=="__main__":
    app.run(debug=True)
