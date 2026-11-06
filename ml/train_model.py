
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "accounts.csv"
MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

# Load dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Input features
FEATURES = [
    "profile pic",
    "nums/length username",
    "fullname words",
    "nums/length fullname",
    "name==username",
    "description length",
    "external URL",
    "private",
    "#posts",
    "#followers",
    "#follows"
]

TARGET = "fake"

# Check columns
missing = [col for col in FEATURES + [TARGET] if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Prepare data
X = df[FEATURES].apply(pd.to_numeric, errors="coerce")
y = pd.to_numeric(df[TARGET], errors="coerce")

valid_rows = y.notna()
X = X.loc[valid_rows]
y = y.loc[valid_rows].astype(int)

if not set(y.unique()).issubset({0, 1}):
    raise ValueError("Target must contain only 0 and 1.")

print("Dataset shape:", X.shape)
print("\nAccount distribution:")
print(y.value_counts())

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create model
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    ))
])

# Train
print("\nTraining the Random Forest model...")
model.fit(X_train, y_train)

# Predict test data
predictions = model.predict(X_test)

# Evaluate
print("\n========== MODEL RESULTS ==========")

print("Accuracy:",
      round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("Precision:",
      round(precision_score(y_test, predictions, zero_division=0), 3))

print("Recall:",
      round(recall_score(y_test, predictions, zero_division=0), 3))

print("F1 Score:",
      round(f1_score(y_test, predictions, zero_division=0), 3))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Save trained model
joblib.dump({
    "model": model,
    "features": FEATURES
}, MODEL_PATH)

print("\nModel trained and saved successfully!")
print("Saved at:", MODEL_PATH)

