# app.py

from flask import Flask, request, jsonify
from fetcher import fetch_emails
from rules import classify_email
from main import classify_with_model, load_model
import json
import re

app = Flask(__name__)
model, vectorizer = load_model()

# Helper function to extract dates from subject (basic example)
def extract_datetime_from_subject(subject):
    match = re.search(r'(\d{1,2}[:.]\d{2})|(\d{1,2}/\d{1,2}/\d{2,4})', subject)
    return match.group(0) if match else None

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if email and password:
        return jsonify({"message": "Login data received"}), 200
    return jsonify({"error": "Missing credentials"}), 400

@app.route('/fetch_emails', methods=['POST'])
def fetch():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    courses = data.get('courses', [])

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    emails = fetch_emails(email, password, limit=50)
    filtered = []

    for e in emails:
        if model:
            label = classify_with_model(e['subject'], e['sender'], model, vectorizer)
        else:
            label = classify_email(e['subject'], e['sender'])

        date_info = extract_datetime_from_subject(e['subject'])

        filtered.append({
            'subject': e['subject'],
            'sender': e['sender'],
            'date': str(e['date']),
            'label': label,
            'event_time': date_info
        })

    return jsonify(filtered), 200

@app.route('/notify', methods=['POST'])
def notify():
    # Placeholder endpoint for future push notification hook
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)
