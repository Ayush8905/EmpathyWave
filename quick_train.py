import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

# Load and prepare data
print("Loading data...")
df = pd.read_csv('augmented_dataset_75000.csv')
df['binary_label'] = (df['label'] == 2).astype(int)

# Use smaller sample for quick training
df_sample = df.sample(n=10000, random_state=42)
texts = df_sample['text'].astype(str).tolist()
labels = df_sample['binary_label'].tolist()

print(f"Training on {len(texts)} samples")

# Split data
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Vectorize
vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train
model = RandomForestClassifier(n_estimators=5, random_state=42)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

# Save
os.makedirs('data/models', exist_ok=True)
joblib.dump({'model': model, 'vectorizer': vectorizer}, 'data/models/text_model.pkl')
print("Model saved to data/models/text_model.pkl")
