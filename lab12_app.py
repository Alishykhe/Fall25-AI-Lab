from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model and encoders
with open('models/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

with open('models/features.pkl', 'rb') as f:
    features = pickle.load(f)

with open('models/info.pkl', 'rb') as f:
    model_info = pickle.load(f)

@app.route('/')
def home():
    manufacturers = encoders['Manufacturer'].classes_.tolist()
    models_list = encoders['Model'].classes_.tolist()
    fuel_types = encoders['Fuel type'].classes_.tolist()
    
    return render_template('index.html', 
                         manufacturers=manufacturers,
                         models=models_list,
                         fuel_types=fuel_types,
                         r2_score=model_info['r2_score'],
                         mae=model_info['mae'])

@app.route('/predict', methods=['POST'])
def predict():
    manufacturer = request.form['manufacturer']
    model_name = request.form['model']
    engine_size = float(request.form['engine_size'])
    fuel_type = request.form['fuel_type']
    year = int(request.form['year'])
    mileage = int(request.form['mileage'])
    
    manufacturer_encoded = encoders['Manufacturer'].transform([manufacturer])[0]
    model_encoded = encoders['Model'].transform([model_name])[0]
    fuel_encoded = encoders['Fuel type'].transform([fuel_type])[0]
    
    vehicle_age = 2025 - year
    mileage_per_year = mileage / (vehicle_age + 1)
    
    input_data = pd.DataFrame([[
        manufacturer_encoded,
        model_encoded,
        engine_size,
        fuel_encoded,
        year,
        mileage,
        vehicle_age,
        mileage_per_year
    ]], columns=features)
    
    prediction = model.predict(input_data)[0]
    
    manufacturers = encoders['Manufacturer'].classes_.tolist()
    models_list = encoders['Model'].classes_.tolist()
    fuel_types = encoders['Fuel type'].classes_.tolist()
    
    return render_template('index.html',
                         manufacturers=manufacturers,
                         models=models_list,
                         fuel_types=fuel_types,
                         r2_score=model_info['r2_score'],
                         mae=model_info['mae'],
                         prediction=f'${prediction:,.2f}',
                         input_data={
                             'manufacturer': manufacturer,
                             'model': model_name,
                             'engine_size': engine_size,
                             'fuel_type': fuel_type,
                             'year': year,
                             'mileage': mileage
                         })

if __name__ == '__main__':
    app.run(debug=True)
