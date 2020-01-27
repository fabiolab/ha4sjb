import click
from loguru import logger
from ha4sjb.HelloAssoAdapter import HelloAssoAdapter
from ha4sjb.GoogleSpreadSheet import GoogleSpreadSheet
from ha4sjb.GoogleDrive import GoogleDrive
from datetime import datetime
from ha4sjb.HelloAssoApi import HelloAssoApi
import os

GOOGLE_SPREADSHEET = "Adhérents 2019/2020"  # Must be shared with the user set in credentials.json

logger.add("file_{time}.log")
logger.debug(os.getenv("ORGANIZATION_ID"))


@click.command()
@click.argument("date_from", type=click.DateTime())
def ha2google(date_from: datetime):
    api_ha = HelloAssoApi()
    actions = api_ha.get_actions(date_from)

    adapter = HelloAssoAdapter()
    data = adapter.load_from_apiresponse(actions)

    google_spreadsheet = GoogleSpreadSheet(GOOGLE_SPREADSHEET)
    google_spreadsheet.import_rows(data)

    # google_drive = GoogleDrive()
    # google_drive.upload_pdf_file("data/amandine.pdf", "BRAULT_Amandine_Certif.pdf")


if __name__ == "__main__":
    ha2google()
