import datetime
import subprocess

import json

def send_notification():
    """Send a notification using cURL."""
    payload = {
        "project": "YourProjectName",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test": "BackupSuccessful"
    }
    print("Sending notification...")
    subprocess.run([
        "curl", "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
        "https://webhook.site/21a05cab-b92b-419f-a6a0-f67f54275879"
    ])
    print("Notification sent.")
