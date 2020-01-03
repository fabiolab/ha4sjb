from loguru import logger
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"


class GoogleSpreadSheet:

    def __init__(self, spreadsheet: str):
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        self.sheet = client.open(spreadsheet).sheet1  # Open the spreadhseet

    def import_rows(self, data):
        for item in data:
            self.sheet.append_row(item)
