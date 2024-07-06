import pickle
from flask import Blueprint, render_template, request
from beautyHaven.products.models import Product, Label
from beautyHaven import app 
recommend_routes = Blueprint('recommend_routes', __name__)

def load_model():
    model_path = 'model.pkl'
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

def map_skin_type_to_category(skin_type):
    categories = {
        'Combination': 0,
        'Dry': 1,
        'Normal': 2,
        'Oily': 3,
        'Sensitive': 4
    }
    return categories.get(skin_type, -1) 

@recommend_routes.route('/recommend', methods=['GET', 'POST'])
def recommend_products():
    if request.method == 'POST':
        skin_type = request.form['skin_type']
        print(f"User-selected skin type: {skin_type}")

        category = map_skin_type_to_category(skin_type)
        if category == -1:
            return "Invalid skin type" 
        
        print(f"Mapped category: {category}")

        predicted_skin_type = model.predict([[category]])[0] 
        print(f"Predicted skin type: {predicted_skin_type}") 

        
        label = Label.query.filter_by(name=skin_type).first()
        print(f"Label found: {label}")
        if label:
            recommended_products = Product.query.filter_by(label_id=label.id).all()
            print(f"Number of products found: {len(recommended_products)}")
        else:
            recommended_products = []

        recommendations = []
        for product in recommended_products:
            recommendations.append({
                'id': product.id,
                'brand': product.brand.name,
                'name': product.name,
                'price': product.price,
                'image_1': product.image_1,
                'description': product.description,
                'discount': product.discount
            })
        return render_template('recommendations.html', skin_type=skin_type, recommendations=recommendations)
    return render_template('recommend.html')