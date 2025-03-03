'''import pickle
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the trained model and LabelEncoders
with open('random_forest_model.pkl', 'rb') as model_file:
    rf_classifier = pickle.load(model_file)

with open('label_encoders.pkl', 'rb') as le_file:
    label_encoders = pickle.load(le_file)

# Define categorical columns (consistent with training)
categorical_cols = ['merchant', 'category', 'gender', 'job']  # Removed 'lat', 'long', 'city_pop'

# Define the features used for training (important!)
features = ['merchant', 'category', 'amt', 'gender', 'job'] # Removed 'lat', 'long', 'city_pop'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from the form
    merchant = request.form['merchant']
    category = request.form['category']
    amt = float(request.form['amt'])
    gender = request.form['gender']
    job = request.form['job']
    # Removed: lat = float(request.form['lat'])
    # Removed: long = float(request.form['long'])
    # Removed: city_pop = float(request.form['city_pop'])

    # Create input DataFrame (using only the trained features)
    input_data = pd.DataFrame({
        'merchant': [merchant],
        'category': [category],
        'amt': [amt],
        'gender': [gender],
        'job': [job]
    })

    # Transform categorical features (handling unseen values)
    for col in categorical_cols:
        if col in input_data.columns:
            if input_data[col].dtype == object:
                if input_data[col].iloc[0] in label_encoders[col].classes_:
                    input_data[col] = label_encoders[col].transform(input_data[col])
                else:
                    input_data[col] = label_encoders[col].transform(['unknown']) # Use 'unknown' for unseen values
                input_data[col] = input_data[col].astype(int) #convert the column to integer type

    # Make prediction (using the trained features)
    prediction = rf_classifier.predict(input_data[features]) # Use only trained features

    return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)'''
import pickle
from flask import Flask, render_template, request
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
uri = "mongodb+srv://user:12345@myfirstcluster.eifhy.mongodb.net/?retryWrites=true&w=majority&appName=myFirstCluster"
client = MongoClient(uri)
db_name = client["fraud_detection"]  # Database name
col = db_name["dataa"]  # Collection name

# Load the trained model and LabelEncoders
with open('random_forest_model.pkl', 'rb') as model_file:
    rf_classifier = pickle.load(model_file)

with open('label_encoders.pkl', 'rb') as le_file:
    label_encoders = pickle.load(le_file)

# Define categorical columns (consistent with training)
categorical_cols = ['merchant', 'category', 'gender', 'job']  # Removed 'lat', 'long', 'city_pop'

# Define the features used for training (important!)
features = ['merchant', 'category', 'amt', 'gender', 'job']  # Removed 'lat', 'long', 'city_pop'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from the form
    merchant = request.form['merchant']
    category = request.form['category']
    amt = float(request.form['amt'])
    gender = request.form['gender']
    job = request.form['job']

    # Create input DataFrame (using only the trained features)
    input_data = pd.DataFrame({
        'merchant': [merchant],
        'category': [category],
        'amt': [amt],
        'gender': [gender],
        'job': [job]
    })

    # Transform categorical features (handling unseen values)
    for col_name in categorical_cols:
        if col_name in input_data.columns:
            if input_data[col_name].dtype == object:
                if input_data[col_name].iloc[0] in label_encoders[col_name].classes_:
                    input_data[col_name] = label_encoders[col_name].transform(input_data[col_name])
                else:
                    input_data[col_name] = label_encoders[col_name].transform(['unknown'])  # Use 'unknown' for unseen values
                input_data[col_name] = input_data[col_name].astype(int)  # Convert to integer type

    # Make prediction (using the trained features)
    prediction = rf_classifier.predict(input_data[features])  # Use only trained features

    # Prepare the user data to insert into MongoDB as a DataFrame
    user_data = pd.DataFrame({
        'merchant': [merchant],
        'category': [category],
        'amt': [amt],
        'gender': [gender],
        'job': [job],
        'prediction': prediction[0]  # Store the prediction result
    })

    # Convert the DataFrame to a dictionary and insert into MongoDB
    user_data_dict = user_data.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
    col.insert_many(user_data_dict)  # Insert the data into MongoDB

    # Return the prediction along with the stored data
    return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
