import pickle
import os
import pandas as pd
from flask import Blueprint, render_template, request
from beautyHaven.products.models import Product, Label

recommend_routes = Blueprint('recommend_routes', __name__)

def load_model():
    model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'model.pkl')
    if not os.path.isfile(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

def predict_products_for_skin_type(data, skin_type, min_price=None, max_price=None, min_rank=None, brand=None):
    suitable_products = data[data['SkinType'] == skin_type]
    
    if min_price is not None:
        suitable_products = suitable_products[suitable_products['Price'] >= min_price]
    if max_price is not None:
        suitable_products = suitable_products[suitable_products['Price'] <= max_price]
    if min_rank is not None:
        suitable_products = suitable_products[suitable_products['Rank'] >= min_rank]
    if brand:
        suitable_products = suitable_products[suitable_products['Brand'].str.lower() == brand.lower()]
        
    return suitable_products

@recommend_routes.route('/recommend', methods=['GET', 'POST'])
def recommend_products():
    if request.method == 'POST':
        skin_type = request.form['skin_type']
        min_price = request.form.get('min_price', type=float)
        max_price = request.form.get('max_price', type=float)
        min_rank = request.form.get('min_rank', type=float)
        brand = request.form.get('brand', '').strip() or None

        base_dir = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.join(base_dir, '..', 'cosmetics.csv')

        if not os.path.isfile(csv_path):
            return "CSV file not found."

        data = pd.read_csv(csv_path)

        # Ensure 'SkinType' column is created
        if 'SkinType' not in data.columns:
            data['SkinType'] = data[['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']].idxmax(axis=1)

        try:
            suitable_products = predict_products_for_skin_type(data, skin_type, min_price, max_price, min_rank, brand)
            
            # Debugging: Print columns to check if they exist in suitable_products
            print("Columns in suitable_products DataFrame:", suitable_products.columns)

            recommendations = []
            for _, row in suitable_products.iterrows():
                recommendations.append({
                    'brand': row.get('Brand', 'N/A'),
                    'name': row.get('Name', 'N/A'),
                    'price': row.get('Price', 'N/A'),
                    'rank': row.get('Rank', 'N/A'),
                    'ingredients': row.get('Ingredients', 'N/A')
                })

            return render_template('recommendations.html', skin_type=skin_type, recommendations=recommendations)

        except Exception as e:
            return f"Prediction error: {e}"

    return render_template('recommend.html')

