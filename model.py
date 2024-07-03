import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

file_path = 'cosmetics.csv'
data = pd.read_csv(file_path)

data['SkinType'] = data[['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']].idxmax(axis=1)

features = data[['Price']]
target = data['SkinType']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)




with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
