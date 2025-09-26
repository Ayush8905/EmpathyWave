import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load data
df = pd.read_csv('augmented_dataset_75000.csv')
print('Dataset loaded:', df.shape)

# Prepare labels (convert 2->1, 0->0)
df['binary_label'] = (df['label'] == 2).astype(int)
print('Label distribution:', df['binary_label'].value_counts().to_dict())

# Clean data
df_clean = df.dropna(subset=['text', 'binary_label'])
texts = df_clean['text'].astype(str).tolist()
labels = df_clean['binary_label'].tolist()

# Split data
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Vectorize
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

# Save
joblib.dump({'model': model, 'vectorizer': vectorizer}, 'data/models/text_model.pkl')
print('Model saved!')
