import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# setup credentials
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("customer info").sheet1


def save_to_sheet(user):
    sheet.append_row([
        user.get("name"),
        user.get("phone"),
        user.get("interest"),
        datetime.utcnow().isoformat()
    ])