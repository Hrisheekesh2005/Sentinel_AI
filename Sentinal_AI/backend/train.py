import pandas as pd
import pickle # Changed from joblib to match agent.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Load dataset
# Ensure 'scam_data.csv' is in the same folder as this script
try:
    data = pd.read_csv("scam_data.csv")
    X = data["text"]
    y = data["label"]

    # 2. Vectorizer
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    # 3. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42
    )

    # 4. Model (Logistic Regression is great for probability scores)
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test)
    print("--- Model Accuracy Report ---")
    print(classification_report(y_test, y_pred))

    # 6. Save using PICKLE (Required to match agent.py)
    pickle.dump(model, open("model.pkl", "wb"))
    pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

    print("✅ Success: model.pkl and vectorizer.pkl generated using Pickle.")

except FileNotFoundError:
    print("❌ Error: 'scam_data.csv' not found. Please place it in the backend folder.")
except Exception as e:
    print(f"❌ An error occurred: {e}")