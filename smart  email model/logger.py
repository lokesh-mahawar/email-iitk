import csv
import os

CSV_FILE = 'dataset.csv'

def log_to_csv(emails):
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['subject', 'sender', 'label'])

        if not file_exists:
            writer.writeheader()

        for email in emails:
            writer.writerow({
                'subject': email['subject'],
                'sender': email['sender'],
                'label': email['label']
            })
