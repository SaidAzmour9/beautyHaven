import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv('cosmetics.csv')

data['SkinType'] = data[['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']].idxmax(axis=1)

features = data[['Price', 'Rank']] 
target = data['SkinType']


X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy}')

with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)
