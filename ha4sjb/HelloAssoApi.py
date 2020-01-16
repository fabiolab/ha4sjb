from loguru import logger
import requests
import pendulum
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime

HOST = "api.helloasso.com"
ENDPOINT = "/v3"
RESULT_PER_PAGE = 500
ACTIONS_ROUTE = f"/organizations/{os.getenv('ORGANIZATION_ID')}/campaigns/{os.getenv('CAMPAIGN_ID')}/actions.json"


class HelloAssoApi:

    def __init__(self):
        pass

    @staticmethod
    def get_actions(from_date: datetime = pendulum.datetime(2019, 7, 1)) -> list:
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
