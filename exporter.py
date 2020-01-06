import click
from loguru import logger
from ha4sjb.HelloAssoAdapter import HelloAssoAdapter
from ha4sjb.GoogleSpreadSheet import GoogleSpreadSheet
from ha4sjb.GoogleDrive import GoogleDrive
from datetime import datetime

GOOGLE_SPREADSHEET = "HelloAsso Adhérents 2019-2020"  # Must be shared with the user set in credentials.json


@click.command()
@click.argument("csv_file", type=click.Path(exists=True, file_okay=True))
@click.argument("date_from", type=click.DateTime())
def ha2google(csv_file: str, date_from: datetime):
    adapter = HelloAssoAdapter()
    adapter.load_from_helloasso(csv_file, date_from)
    data = adapter.export_to_google()

    google_spreadsheet = GoogleSpreadSheet(GOOGLE_SPREADSHEET)
    google_spreadsheet.import_rows(data)

    # google_drive = GoogleDrive()
    # google_drive.upload_pdf_file("data/amandine.pdf", "BRAULT_Amandine_Certif.pdf")


if __name__ == "__main__":
    ha2google()
