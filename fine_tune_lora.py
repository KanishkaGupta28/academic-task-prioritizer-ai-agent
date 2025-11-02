# fine_tune_lora.py — lightweight fine-tuning simulation for the Academic Task Prioritizer

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

# Load dataset
df = pd.read_csv("tasks_dataset.csv")

# Encode Priority as numeric target
priority_map = {"Low": 1, "Medium": 2, "High": 3}
df["Priority_Level"] = df["Priority"].map(priority_map)

# Define features and target
X = df[["Difficulty", "Importance"]]
y = df["Priority_Level"]

# Split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a small regression model (simulating LoRA fine-tuning)
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)

print("✅ Fine-tuning complete!")
print(f"Model R² Score (Reliability): {score:.2f}")

# Save model coefficients
joblib.dump(model, "fine_tuned_model.pkl")
print("💾 Model saved as fine_tuned_model.pkl")
