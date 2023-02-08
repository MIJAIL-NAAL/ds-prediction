from flask import (
    Blueprint, render_template, request
)
from flask_cors import CORS, cross_origin
import joblib
import pandas as pd


bp = Blueprint('prediction', __name__)

@bp.route('/', methods=['GET'])
@cross_origin()
def home_page():
    return render_template("index.html", static_url_path='/static')

@bp.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    try:
        #  reading the inputs given by the user
        Pregnancies=int(request.form['Pregnancies'])
        Glucose = float(request.form['Glucose'])
        BloodPressure = float(request.form['BloodPressure'])
        SkinThickness = float(request.form['SkinThickness'])
        Insulin = float(request.form['Insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
        Age = int(request.form['Age'])
        feat_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI',
                        'DiabetesPedigreeFunction', 'Age']
        
        scaler = joblib.load('models/scaler.joblib')
        model = joblib.load('models/model.joblib')

        row = [Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age]
        
        df = pd.DataFrame([row], columns=feat_cols)
        X = scaler.transform(df)
        data = pd.DataFrame(X, columns=feat_cols)

        # predictions using the loaded model file
        prediction = model.predict_proba(data)
        # showing the prediction results in a UI
        return render_template('predict.html', prediction=round(100*prediction[0][1]))
    
    except Exception as e:
        return('The Exception message is: ', e)

# run locally with commnad: flask --app ds_app --debug run