from loguru import logger
import requests
import pendulum
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime, date

HOST = "api.helloasso.com"
ENDPOINT = "/v3"
RESULT_PER_PAGE = 500
ACTIONS_ROUTE = f"/organizations/{os.getenv('ORGANIZATION_ID')}/campaigns/{os.getenv('CAMPAIGN_ID')}/actions.json"


def _get_season_start_date(current_date: date = pendulum.now()) -> date:
    """
        Get the start date of the current season.

        :Example:
        >>> _get_season_start_date(pendulum.date(2019, 8, 2))
        Date(2019, 7, 1)
        >>> g_et_season_start_date(pendulum.date(2019, 4, 28))
        Date(2018, 7, 1)
    """
    start_date = pendulum.date(current_date.year, 7, 1)
    if current_date.month < 7:
        start_date = start_date.subtract(years=1)

    return start_date


class HelloAssoApi:

    def __init__(self):
        ...

    @staticmethod
    def get_actions(from_date: datetime = _get_season_start_date()) -> list:
        params = {
            "from": from_date,
            "results_per_page": 500
        }
        url = f"https://{HOST}{ENDPOINT}{ACTIONS_ROUTE}"
        response = requests.request("GET", url, params=params,
                                    auth=HTTPBasicAuth(os.getenv('API_USER'), os.getenv('API_KEY')))

        if response.status_code >= 400:
            logger.error(f"Can't get a response from {url}")
            return []

        body = response.json().get('resources', [])
        logger.debug(body)
        logger.debug(f"{len(body)} action(s) recorded from {from_date}")
        return body
