import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
df = pd.read_csv('MLmodel/crop_recommendation.csv')

# Split features and target
features = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
target = df['label']

# Splitting into train and test data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=2)

# Train Random Forest classifier
RF = RandomForestClassifier(n_estimators=16, random_state=2)
RF.fit(X_train, y_train)

# Evaluate model
predicted_values = RF.predict(X_test)
accuracy = accuracy_score(y_test, predicted_values)
print("Random Forest's Accuracy is:", accuracy)
print(classification_report(y_test, predicted_values))

# Save trained model
with open('./RandomForest.pkl', 'wb') as file:
    pickle.dump(RF, file)
