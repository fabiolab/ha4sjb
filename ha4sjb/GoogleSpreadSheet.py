from loguru import logger
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = "credentials.json"
RECORD_ID_COL = 1


class GoogleSpreadSheet:

    def __init__(self, spreadsheet: str):
        with open(CREDENTIALS_FILE, 'w') as credentials_file:
            json.dump(os.getenv('GOOGLE_CREDENTIALS'), credentials_file)

        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        logger.info(f"Opening {spreadsheet} for writing")
        self.sheet = client.open(spreadsheet).sheet1  # Open the spreadhseet

    def import_rows(self, data):
        item_counter = 0
        for item in data:
            if item[0] not in self.sheet.col_values(RECORD_ID_COL):
                item_counter += 1
                self.sheet.append_row(item)
                logger.info(f"{item[3]} {item[4]} added to {self.sheet.spreadsheet}")

        logger.info(f"{item_counter} items added to {self.sheet.spreadsheet}")
        logger.info(f"{len(data)} items in HelloAsso")
