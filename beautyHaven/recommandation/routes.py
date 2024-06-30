import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Blueprint, render_template, request
from beautyHaven.products.models import Product
import pandas as pd
import os

recommend_routes = Blueprint('recommend_routes', __name__)

def load_model():
    model_path = 'model.pkl'
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    else:
        print(f"Model file '{model_path}' not found.")
        return None

vectorizer = TfidfVectorizer()

@recommend_routes.route('/recommend', methods=['GET', 'POST'])
def recommend_products():
    global vectorizer
    if request.method == 'POST':
        model = load_model()
        if not model:
            return "Error loading recommendation model."

        df = pd.read_csv('cosmetics.csv')
        df['Text_Features'] = df['Brand'] + " " + df['Name'] + " " + df['Ingredients']
        
        # Fit vectorizer if not already fitted
        if not hasattr(vectorizer, 'vocabulary_'):
            vectorizer.fit(df['Text_Features'])
        
        # Debug prints
        print(f"Vectorizer vocabulary: {vectorizer.vocabulary_}")

        skin_type = request.form.get('skin_type')
        print(f"Received skin type: {skin_type}")  # Debug

        user_text = f"{skin_type}"
        user_features = vectorizer.transform([user_text])

        predicted_category = model.predict(user_features)[0]
        print(f"Predicted category: {predicted_category}")  # Debug

        # Retrieve recommended products based on predicted category
        recommended_products = Product.query.filter_by(category_id=predicted_category).order_by(Product.price.desc()).limit(3).all()
        print(f"Number of products found: {len(recommended_products)}")  # Debug

        if recommended_products:
            recommendations = [{
                'name': product.name,
                'brand': product.brand.name,
                'category': product.category.name,
                'price': product.price
            } for product in recommended_products]
            return render_template('recommendations.html', recommendations=recommendations)
        else:
            return f"No recommendations found for category {predicted_category}."  # More informative message

    return render_template('recommend.html')
