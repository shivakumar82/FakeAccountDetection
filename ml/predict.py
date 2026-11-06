
import joblib
import pandas as pd
from pathlib import Path

# Load trained model
MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

saved = joblib.load(MODEL_PATH)
model = saved["model"]
FEATURES = saved["features"]


def explain_account(account_data):
    indicators = []

    # Check profile picture
    if account_data.get("profile pic") == 0:
        indicators.append("No profile picture detected.")

    # Check username structure
    username_ratio = account_data.get("nums/length username")
    if username_ratio is not None and username_ratio > 0.5:
        indicators.append("Username contains a high proportion of numbers.")

    # Check profile description
    description = account_data.get("description length")
    if description is not None and description < 10:
        indicators.append("Profile description is very short.")

    # Check number of posts
    posts = account_data.get("#posts")
    if posts is not None and posts < 5:
        indicators.append("Very few posts found on the account.")

    # Compare followers and following
    followers = account_data.get("#followers")
    follows = account_data.get("#follows")

    if followers is not None and follows is not None:
        if follows > 500 and follows > max(followers, 1) * 5:
            indicators.append(
                "Following count is much higher than follower count."
            )

    # Check username and full name similarity
    name_match = account_data.get("name==username")
    if name_match == 1:
        indicators.append(
            "Full name and username are identical."
        )

    return indicators


def predict_account(account_data):

    # Prepare account data
    account = pd.DataFrame(
        [[account_data.get(feature) for feature in FEATURES]],
        columns=FEATURES
    )

    account = account.apply(pd.to_numeric, errors="coerce")

    # Predict account
    prediction = int(model.predict(account)[0])

    probabilities = model.predict_proba(account)[0]
    classes = list(model.classes_)

    fake_probability = float(
        probabilities[classes.index(1)]
    )

    risk_score = round(fake_probability * 100, 2)

    # Risk level
    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Explain using the same normalized numeric values sent to the model.
    normalized_account = {
        feature: account.iloc[0][feature]
        for feature in FEATURES
    }
    indicators = explain_account(normalized_account)

    return {
        "prediction": "Suspicious" if prediction == 1 else "Genuine",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "indicators": indicators
    }


# Test account
if __name__ == "__main__":

    sample_account = {
        "profile pic": 0,
        "nums/length username": 0.4,
        "fullname words": 1,
        "nums/length fullname": 0.5,
        "name==username": 1,
        "description length": 5,
        "external URL": 0,
        "private": 0,
        "#posts": 3,
        "#followers": 20,
        "#follows": 1500
    }

    result = predict_account(sample_account)

    print("\n===== FAKE ACCOUNT DETECTION =====")
    print("Prediction:", result["prediction"])
    print("Risk Score:", result["risk_score"], "%")
    print("Risk Level:", result["risk_level"])

    print("\n===== EXPLANATION =====")

    if result["indicators"]:
        for indicator in result["indicators"]:
            print("-", indicator)
    else:
        print("No predefined warning indicators detected.")

    print("\nNote: These indicators are warnings, not proof.")
