import click
import pendulum
from loguru import logger
from ha4sjb.HelloAssoAdapter import HelloAssoAdapter
from ha4sjb.GoogleSpreadSheet import GoogleSpreadSheet
from datetime import datetime
from ha4sjb.HelloAssoApi import HelloAssoApi
import os

# GOOGLE_SPREADSHEET = "Adhérents 2020/2021"  # Must be shared with the user set in credentials.json
# GOOGLE_SPREADSHEET = "Test HelloAsso Adhérents 2020-2021"  # Must be shared with the user set in credentials.json

REQUIRED_ENV_VARIABLES = ['ORGANIZATION_ID', 'CAMPAIGN_ID', 'GOOGLE_SPREADSHEET']


@click.command()
@click.option("--from_date", required=False, type=click.DateTime())
def ha2google(from_date: datetime):
    if not from_date:
        from_date = pendulum.datetime(2020, 1, 1)

    api_ha = HelloAssoApi()
    actions = api_ha.get_actions(from_date)

    adapter = HelloAssoAdapter()
    data = adapter.load_from_apiresponse(actions)

    google_spreadsheet = GoogleSpreadSheet(os.getenv('GOOGLE_SPREADSHEET'))
    google_spreadsheet.import_rows(data)


def _check_env_variables():
    for env_var in REQUIRED_ENV_VARIABLES:
        if not os.getenv(env_var):
            message = f"Mandatory environment variable {env_var} is not set"
            logger.error(message)
            raise ValueError(message)
        else:
            logger.info(f"{env_var} = {os.getenv(env_var)}")


if __name__ == "__main__":
    _check_env_variables()
    ha2google()
