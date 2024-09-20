import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = pd.read_csv('cosmetics.csv')

# Determine the skin type based on the max value of each skin type column
data['SkinType'] = data[['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']].idxmax(axis=1)

# Define features and target
features = data[['Price', 'Rank']]
target = data['SkinType']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions and calculate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy}')


with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
    print("Model saved to 'model.pkl'.")