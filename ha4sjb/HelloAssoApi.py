from loguru import logger
import requests
import pendulum
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime, date

HOST = "api.helloasso.com"
ENDPOINT = "/v3"
RESULT_PER_PAGE = 100
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
    def get_actions_by_page(from_date: date = _get_season_start_date(), page: int = 1) -> list:
        params = {
            "from": from_date,
            "results_per_page": RESULT_PER_PAGE,
            "page": page
        }
        url = f"https://{HOST}{ENDPOINT}{ACTIONS_ROUTE}"
        logger.info(f"Call {url}")
        response = requests.request("GET", url, params=params,
                                    auth=HTTPBasicAuth(os.getenv('API_USER'), os.getenv('API_KEY')))

        if response.status_code >= 400:
            logger.error(f"Can't get a response from {url}")
            logger.error(f"{response.status_code}/{response.reason}")
            return []

        body = response.json().get('resources', [])
        logger.debug(body)
        logger.info(f"{len(body)} action(s) recorded from {from_date}")
        return body

    @staticmethod
    def get_actions(from_date: date = _get_season_start_date()) -> list:
        page = 1
        actions = HelloAssoApi.get_actions_by_page(from_date)
        next_page_actions = actions
        while next_page_actions:
            page += 1
            next_page_actions = HelloAssoApi.get_actions_by_page(from_date=from_date, page=page)
            actions += next_page_actions
        return actions

    @staticmethod
    def get_file(url: str):
        logger.info(f"Call {url}")
        API_KEY = "w5Hg7H5QqM94vxBDvn52Z"
        API_USER = "saint - jacques - badminton"

        response = requests.request("GET", url, auth=HTTPBasicAuth(API_USER, API_KEY))

        if response.status_code >= 400:
            logger.error(f"Can't get a response from {url}")
            return []

        body = response.json().get('resources', [])
        logger.debug(body)
        logger.info(f"{len(body)} action(s)")
        return body
