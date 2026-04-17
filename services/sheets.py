import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 🔥 Load credentials from Render env
creds_json = os.environ.get("GOOGLE_CREDS")

if not creds_json:
    raise Exception("GOOGLE_CREDS not found in environment variables")

creds_dict = json.loads(creds_json)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

client = gspread.authorize(creds)

sheet = client.open("customer info").sheet1


def save_to_sheet(user):
    sheet.append_row([
        user.get("name", ""),
        user.get("phone", ""),
        user.get("interest", ""),
        datetime.utcnow().isoformat()
    ])