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


## 1. Imports and Constants
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
```
## Imports: Required libraries for file operations, subprocess execution, argument parsing, and JSON handling.
Constants:
          BACKUP_FOLDER: Directory to store backup files.
          ROTATION_DAYS, ROTATION_WEEKS, ROTATION_MONTHS: Retention periods for daily, weekly, and monthly backups.
          GOOGLE_DRIVE_REMOTE, GOOGLE_DRIVE_FOLDER: Configuration for Google Drive uploads via rclone.
