
from pathlib import Path

# Use the currently opened project folder
project = Path(".")

folders = ["data", "ml"]

files = {
    "data/accounts.csv": "",
    "ml/train_model.py": "# Machine learning model training code\n",
    "ml/predict.py": "# Fake account prediction code\n",
    "requirements.txt": """pandas
numpy
scikit-learn
matplotlib
seaborn
joblib
""",
    "README.md": "# Fake Social Media Account Detection\n"
}

for folder in folders:
    (project / folder).mkdir(exist_ok=True)

for filename, content in files.items():
    path = project / filename
    if not path.exists():
        path.write_text(content, encoding="utf-8")

print("All project folders and files created successfully!")

