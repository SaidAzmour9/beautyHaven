import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Load data
df = pd.read_csv('cosmetics.csv')

# Preprocess data
df['Text_Features'] = df['Brand'] + " " + df['Name'] + " " + df['Ingredients']
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(df['Text_Features'])

# Define target labels
target_labels = {
    'Moisturizer': 0,
    'Sun protect': 1,
    'Serum': 2,
    'Cleanser': 3,
    'Face Mask': 4,
    'Treatment': 5,
    'Eye cream': 6
}
encoded_targets = df['Label'].map(target_labels)

# Train the SVM model
model = SVC(kernel='linear')  # Linear kernel for interpretability
model.fit(features, encoded_targets)

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
