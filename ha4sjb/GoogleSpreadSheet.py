from loguru import logger
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
RECORD_ID_COL = 1


class GoogleSpreadSheet:

    def __init__(self, spreadsheet: str, credentials: str):
        credentials = json.loads(credentials)

        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, SCOPE)
        client = gspread.authorize(creds)
        logger.info(f"Opening {spreadsheet} for writing")
        self.sheet = client.open(spreadsheet).sheet1  # Open the spreadhseet

    def import_rows(self, data: list) -> list:
        current_ids = self.sheet.col_values(RECORD_ID_COL)
        items = list()
        for item in data:
            if item[0] not in current_ids:
                items.append(item)
                row = len(self.sheet.get_all_values()) + 1
                self.sheet.append_row(item, table_range=f'A{row}')
                logger.info(f"{item[3]} {item[4]} added to {self.sheet.spreadsheet} at position {row}")

        logger.info(f"{len(items)} items added to {self.sheet.spreadsheet}")
        logger.info(f"{len(data)} items in HelloAsso")

        return items
