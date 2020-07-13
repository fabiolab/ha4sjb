import click
import pendulum
from loguru import logger

from ha4sjb.GoogleDrive import GoogleDrive
from ha4sjb.HelloAssoAdapter import HelloAssoAdapter
from ha4sjb.GoogleSpreadSheet import GoogleSpreadSheet
from datetime import datetime
from ha4sjb.HelloAssoApi import HelloAssoApi
import os
import wget

REQUIRED_ENV_VARIABLES = ['ORGANIZATION_ID', 'CAMPAIGN_ID', 'GOOGLE_SPREADSHEET', 'GOOGLE_CREDENTIALS',
                          'GOOGLE_FOLDER_ID']


@click.command()
@click.option("--from_date", required=False, type=click.DateTime())
def run(from_date: datetime):
    ha2google(from_date)


# From HelloAsso to Google Drive/Spreadsheet
def ha2google(from_date: datetime = None):
    _check_env_variables()

    if not from_date:
        from_date = pendulum.datetime(2020, 1, 1)

    api_ha = HelloAssoApi()
    actions = api_ha.get_actions(from_date)

    adapter = HelloAssoAdapter()
    data = adapter.load_from_apiresponse(actions)

    google_spreadsheet = GoogleSpreadSheet(os.getenv('GOOGLE_SPREADSHEET'), os.getenv('GOOGLE_CREDENTIALS'))
    items_added = google_spreadsheet.import_rows(data)

    # FIXME: can't download files from helloasso with the api (authent fails)
    # files_to_transfer = adapter.get_certificates(items_added)
    #
    # googledrive = GoogleDrive(os.getenv('GOOGLE_CREDENTIALS'))
    # googledrive.import_files(files_to_transfer, os.getenv('GOOGLE_FOLDER_ID'), )


def _check_env_variables():
    for env_var in REQUIRED_ENV_VARIABLES:
        if not os.getenv(env_var):
            message = f"Mandatory environment variable {env_var} is not set"
            logger.error(message)
            raise ValueError(message)
        else:
            logger.info(f"{env_var} = {os.getenv(env_var)}")


if __name__ == "__main__":
    run()
