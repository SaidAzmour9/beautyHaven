import pickle
from flask import Blueprint, render_template, request
from beautyHaven.products.models import Product, Label
from beautyHaven import app  # Assuming 'app' is your Flask instance

recommend_routes = Blueprint('recommend_routes', __name__)

# Load the trained model
def load_model():
    model_path = 'model.pkl'
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


model = load_model()

# Function to map skin type to numerical categories (if needed)
def map_skin_type_to_category(skin_type):
    categories = {
        'Combination': 0,
        'Dry': 1,
        'Normal': 2,
        'Oily': 3,
        'Sensitive': 4
    }
    return categories.get(skin_type, -1)  # Handle unknown skin types gracefully

# Flask route to recommend products based on user input
@recommend_routes.route('/recommend', methods=['GET', 'POST'])
def recommend_products():
    if request.method == 'POST':
        skin_type = request.form['skin_type']
        print(f"User-selected skin type: {skin_type}")  # Debugging

        # Map skin type to numerical category (if needed)
        category = map_skin_type_to_category(skin_type)
        if category == -1:
            return "Invalid skin type"  # Handle unknown skin types
        
        print(f"Mapped category: {category}")  # Debugging

        # Make prediction using the model
        predicted_skin_type = model.predict([[category]])[0]  # Assuming your model expects a list/array
        print(f"Predicted skin type: {predicted_skin_type}")  # Debugging

        # Query products from the database based on predicted skin type
        label = Label.query.filter_by(name=skin_type).first()
        print(f"Label found: {label}")  # Debugging
        if label:
            recommended_products = Product.query.filter_by(label_id=label.id).all()
            print(f"Number of products found: {len(recommended_products)}")  # Debugging
        else:
            recommended_products = []

        # Prepare recommendations for rendering
        recommendations = []
        for product in recommended_products:
            recommendations.append({
                'brand': product.brand.name,
                'name': product.name,
                'price': product.price
            })
        # Render the results.html template with recommendations
        return render_template('recommendations.html', skin_type=skin_type, recommendations=recommendations)

    # If request method is GET, render the recommend.html form
    return render_template('recommend.html')