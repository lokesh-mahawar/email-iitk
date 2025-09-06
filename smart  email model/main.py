from config import get_credentials
from fetcher import fetch_emails
from rules import classify_email
from logger import log_to_csv
import time
from datetime import datetime
import os
import pickle
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import sys

MODEL_PATH = 'model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'
SEEN_MSGS_PATH = 'seen_msgs.json'

def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        with open(MODEL_PATH, 'rb') as mf, open(VECTORIZER_PATH, 'rb') as vf:
            model = pickle.load(mf)
            vectorizer = pickle.load(vf)
        print("[INFO] Loaded trained ML model.")
        return model, vectorizer
    else:
        print("[INFO] No ML model found. Using rule-based classification.")
        return None, None

def train_model():
    dataset_path = 'dataset.csv'

    if not os.path.exists(dataset_path):
        print("[WARN] dataset.csv not found. No data to train model.")
        return None, None

    df = pd.read_csv(dataset_path)

    expected_columns = {'subject', 'sender', 'label'}
    if not expected_columns.issubset(set(df.columns.str.strip())):
        print(f"[ERROR] dataset.csv is missing required columns: {expected_columns}")
        return None, None

    df = df.dropna(subset=['subject', 'sender', 'label'])

    if df.empty:
        print("[WARN] dataset.csv has no valid rows. Cannot train model.")
        return None, None

    X = df['subject'].astype(str) + " " + df['sender'].astype(str)
    y = df['label'].astype(str)

    vectorizer = TfidfVectorizer(stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    with open(MODEL_PATH, 'wb') as mf, open(VECTORIZER_PATH, 'wb') as vf:
        pickle.dump(model, mf)
        pickle.dump(vectorizer, vf)

    print("[INFO] ✅ Trained and saved new ML model.")
    return model, vectorizer

def classify_with_model(subject, sender, model, vectorizer):
    text = f"{subject} {sender}"
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

def load_seen_msg_nums():
    if os.path.exists(SEEN_MSGS_PATH):
        with open(SEEN_MSGS_PATH, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_msg_nums(seen_msg_nums):
    with open(SEEN_MSGS_PATH, 'w') as f:
        json.dump(list(seen_msg_nums), f)

def main_loop():
    email, password = get_credentials()
    model, vectorizer = load_model()
    first_run = not os.path.exists(SEEN_MSGS_PATH)
    seen_msg_nums = load_seen_msg_nums()

    if first_run:
        print(f"\n[{datetime.now()}] First run detected. Fetching and labeling all past emails...")
        all_emails = fetch_emails(email, password, limit=None)

        for i, e in enumerate(all_emails, 1):
            e['msg_num'] = i  # simulate message number
            e['label'] = classify_email(e['subject'], e['sender'])

        log_to_csv(all_emails)
        save_seen_msg_nums(set(e['msg_num'] for e in all_emails))

        print(f"[INFO] Stored {len(all_emails)} emails for training.")
        train_model()
        model, vectorizer = load_model()

    # 🔁 Now normal loop begins
    while True:
        print(f"\n[{datetime.now()}] Checking for latest emails...")
        emails = fetch_emails(email, password, limit=50)

        new_emails = []
        next_msg_num = max(seen_msg_nums) + 1 if seen_msg_nums else 1

        for e in emails:
            e['msg_num'] = next_msg_num
            if e['msg_num'] not in seen_msg_nums:
                new_emails.append(e)
                next_msg_num += 1

        if not new_emails:
            print("[INFO] No new emails found.")
        else:
            for e in new_emails:
                if model:
                    e['label'] = classify_with_model(e['subject'], e['sender'], model, vectorizer)
                else:
                    e['label'] = classify_email(e['subject'], e['sender'])

            log_to_csv(new_emails)
            seen_msg_nums.update(e['msg_num'] for e in new_emails)
            save_seen_msg_nums(seen_msg_nums)

            print("\n--- Filtered Emails ---")
            label_map = {'course': '📚 COURSE', 'general': '🗞️ GENERAL', 'scrap': '🗑️ SCRAP'}
            for i, e in enumerate(new_emails, 1):
                label_display = label_map.get(e['label'], e['label'].upper())
                print(f"{i:02d}. [{label_display}] {e['date']} | From: {e['sender']} | Subject: {e['subject']}")

        print("\nSleeping for 5 minutes...\n")
        time.sleep(300)

if __name__ == "__main__":
    main_loop()


if __name__ == "__main__":
    if '--retrain' in sys.argv:
        print("\n[INFO] Manual retraining triggered...")
        train_model()
    else:
        main_loop()
