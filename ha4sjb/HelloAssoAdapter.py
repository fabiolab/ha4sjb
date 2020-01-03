import csv
from loguru import logger
import pendulum
from datetime import datetime

COL_FORMULE = 1
COL_ADHESION = 2
COL_PROMO = 3
COL_NOM = 6
COL_PRENOM = 7
COL_DATE = 9
COL_EMAIL = 10
COL_DATE_NAISSANCE = 11
COL_FACTURE_URL = 12
COL_PHONE = 22
COL_CODE_POSTAL = 23
COL_ADRESSE = 25
COL_VILLE = 27
COL_CRENEAU = 28
COL_IC = 30
COL_CERTIFICAT = 31
COL_QSS = 32

# FIXME : no GENDER COLUMN !!!
COL_GENRE = -1


class HelloAssoAdapter:

    def __init__(self):
        self.items = list()

    def load_from_helloasso(self, csv_file: str, from_date: datetime):
        with open(csv_file, 'r') as input_file:
            reader = csv.reader(input_file, delimiter=';')

            # Skip header
            next(reader)
            self.items = [item for item in reader if
                          pendulum.from_format(item[COL_DATE], "DD/MM/YYYY HH:mm:ss") >= pendulum.instance(from_date)]

            logger.info(f"{len(self.items)} items loaded")

    def export_to_google(self, ) -> list:
        google_items = list()
        for item in self.items:
            google_items.append(self.helloasso_to_google(item))

        return google_items

    @staticmethod
    def helloasso_to_google(item: list) -> list:
        now = pendulum.now()
        google_item = [item[COL_DATE].split()[0],
                       now.format('DD/MM/YYYY'),
                       item[COL_NOM].upper(),
                       item[COL_PRENOM],
                       "?",  # FIXME
                       item[COL_DATE_NAISSANCE],
                       None,
                       item[COL_CRENEAU],
                       "Extérieur" if item[COL_FORMULE] == "Extérieur" else "Licencié",
                       "Oui",
                       None,
                       "Non",
                       None,
                       "Fait",
                       item[COL_IC],
                       item[COL_EMAIL],
                       item[COL_CODE_POSTAL],
                       "Oui",
                       None,
                       "HelloAsso",
                       None,
                       None,
                       None,
                       item[COL_ADHESION]
                       ]
        return google_item
