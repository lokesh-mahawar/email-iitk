# retrain.py

from main import train_model, load_model

print("[INFO] Retraining model from dataset.csv...")
train_model()
load_model()  # Just to verify it loads fine
print("[INFO] ✅ Retrain completed.")
