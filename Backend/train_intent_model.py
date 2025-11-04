import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load intents
with open("intents.json", "r") as file:
    data = json.load(file)

texts = []
labels = []

# Prepare training data
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        texts.append(pattern)
        labels.append(intent["tag"])

# Vectorize text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(labels)

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model and vectorizer
with open("intent_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("✅ Model training complete. Files saved: intent_model.pkl, vectorizer.pkl, label_encoder.pkl")
