# GDrive-Backup-Project
Repository that automates the backup process for the project's code files, implements a rotational backup strategy, and integrates with Google Drive
This Python script automates the backup process for a specified project folder, implements a rotational backup strategy, uploads backups to Google Drive, and sends a notification on successful backup. Below is a detailed explanation of how the script works and how to use it.

## Script Overview
1. Backup Creation:
The script creates a zip file of the specified project folder.
2. Backup Rotation:
It manages and deletes old backups based on a defined retention strategy.
3. Google Drive Upload:
It uploads the created backup to a specified Google Drive folder using rclone.
4. Notification:
It sends a notification to a webhook URL upon successful completion.
## Imports: Required libraries for file operations, subprocess execution, argument parsing, and JSON handling.
Constants:
          BACKUP_FOLDER: Directory to store backup files.
          
          ROTATION_DAYS, ROTATION_WEEKS, ROTATION_MONTHS: Retention periods for daily, weekly, and monthly backups.
          
          GOOGLE_DRIVE_REMOTE, GOOGLE_DRIVE_FOLDER: Configuration for Google Drive uploads via rclone.


## Code
```python
import os
import zipfile
import shutil
import datetime
import subprocess
import argparse
import json

BACKUP_FOLDER = "backups"
ROTATION_DAYS = 7
ROTATION_WEEKS = 4
ROTATION_MONTHS = 3
GOOGLE_DRIVE_REMOTE = "gdrive:"
GOOGLE_DRIVE_FOLDER = "backups"

# Functions
def create_zip(source_folder, output_zip):
    """Create a zip file from the source folder."""
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_folder)
                zipf.write(file_path, arcname)

def delete_old_backups():
    """Delete old backups according to the rotational strategy."""
    now = datetime.datetime.now()
    backup_dirs = [d for d in os.listdir(BACKUP_FOLDER) if os.path.isdir(os.path.join(BACKUP_FOLDER, d))]

    daily_backups = []
    weekly_backups = []
    monthly_backups = []

    for backup in backup_dirs:
        backup_date = datetime.datetime.strptime(backup, "%Y-%m-%d_%H-%M-%S")
        if (now - backup_date).days < ROTATION_DAYS:
            daily_backups.append(backup)
        if (now - backup_date).days // 7 < ROTATION_WEEKS:
            weekly_backups.append(backup)
        if (now - backup_date).days // 30 < ROTATION_MONTHS:
            monthly_backups.append(backup)

    all_backups = sorted(backup_dirs, reverse=True)
    for backup in all_backups:
        if backup not in daily_backups and backup not in weekly_backups and backup not in monthly_backups:
            shutil.rmtree(os.path.join(BACKUP_FOLDER, backup))

def upload_to_google_drive(file_path):
    """Upload the backup file to Google Drive using rclone."""
    subprocess.run(["rclone", "copy", file_path, f"{GOOGLE_DRIVE_REMOTE}/{GOOGLE_DRIVE_FOLDER}"], check=True)

def send_notification():
    """Send a notification using cURL."""
    payload = {
        "project": "YourProjectName",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test": "BackupSuccessful"
    }
    json_payload = json.dumps(payload)
    print("Sending payload:", json_payload)
    try:
        result = subprocess.run([
            "curl", "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", json_payload,
            "https://webhook.site/21a05cab-b92b-419f-a6a0-f67f54275879"
        ], check=True, capture_output=True, text=True)
        print("Notification sent. Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to send notification. Error:", e.stderr)


def main(source_folder):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"{timestamp}.zip"
    zip_path = os.path.join(BACKUP_FOLDER, zip_filename)
    
    # Create zip backup
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    create_zip(source_folder, zip_path)

    # Upload to Google Drive
    upload_to_google_drive(zip_path)

    # Clean old backups
    delete_old_backups()

    # Send notification
    send_notification()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup management script")
    parser.add_argument("source_folder", help="Path to the project folder to be backed up")
    args = parser.parse_args()
    main(args.source_folder)

```


## Script Details
Create Zip: create_zip(source_folder, output_zip)
Delete Old Backups: delete_old_backups()
Upload to Google Drive: upload_to_google_drive(file_path)
Send Notification: send_notification()
Dependencies
Python libraries: os, zipfile, shutil, datetime, subprocess, argparse, json
External tools: rclone, cURL



