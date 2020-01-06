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
COL_GENRE = 22
COL_PHONE = 24
COL_ADRESSE = 25
COL_CODE_POSTAL = 26
COL_VILLE = 27
COL_CRENEAU = 29
COL_IC = 31
COL_CERTIFICAT = 32
COL_QSS = 33

LABEL_EXTERIEUR = "Extérieur"
LABEL_LICENCIE = "Licencié"
LABEL_OUI = "Oui"
LABEL_NON = "Non"
LABEL_FAIT = "Fait"
LABEL_HELLOASSO = "HelloAsso"

MATCH_CRENEAUX = {
    "L1 - Lundi 18h/20h (Milliat/Loisirs)": "L1 Lun - M - 18h - Non encadré",
    "L2 - Lundi 20h/22h15 (Allende/Loisirs)": "L2 Lun - A - 20h - Antoine",
    "L3 - Mercredi 20h/22h15 (Allende/Loisirs)": "L3 Mer - A - 20h - Xavier",
    "L4 - Mercredi 18h30/20h (Milliat/Loisirs)": "L4 Mer - M - 18h30 - Seb",
    "C1 - Mercredi 20h/22h30 (Milliat/Compétiteurs N&R)": "C1 Mer - M - 20h - Seb",
    "C2 - Jeudi 18h30/20h (Milliat/Compétiteurs D&P)": "C2 Jeu - M - 18h30 - Seb",
    "C3 - Jeudi 20h à 22h30 (Milliat/Compétiteurs R&D)": "C3 Jeu - M - 20h - Seb",
    "J1 - Mercredi 13h30/15h (Allende/Poussins & Benjamins)": "J1 Mer - A - 13h30 -  Jérome",
    "J2 - Mercredi 15h/16h30 (Allende/Minimes & Cadets)": "J2 Mer - A - 15h00 - Jérome",
    "J7 - Mercredi 17h/18h (Allende/Minibad)": "J7 Mer - A - 17h - Seb",
    "J3 - Jeudi 17h30/18h30 (Millat/Minibad & poussins confirmés)": "J3 Jeu - M - 17h30 - Seb",
    "J4 - Vendredi 17h15/18h30 (Millat/Poussins/Benjamins)": "J4 Ven - M - 17h15 - Jérome",
    "J5 - Vendredi 18h30/20h00 (Millat/Minimes/Cadets Compétiteurs)": "J5 Ven - M - 18h30 - Jérome",
    "J6 - Samedi 10h30/11h30 (Millat/Minibad/Poussins débutant)": "J6 Sam - M - 10h30 - Killian"
}


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
                       item[COL_GENRE],
                       item[COL_DATE_NAISSANCE],
                       None,
                       MATCH_CRENEAUX[item[COL_CRENEAU]],
                       LABEL_EXTERIEUR if item[COL_FORMULE] == LABEL_EXTERIEUR else LABEL_LICENCIE,
                       LABEL_OUI,
                       None,
                       LABEL_NON,
                       None,
                       LABEL_FAIT,
                       item[COL_IC],
                       item[COL_EMAIL],
                       item[COL_CODE_POSTAL],
                       LABEL_OUI,
                       None,
                       LABEL_HELLOASSO,
                       None,
                       None,
                       None,
                       item[COL_ADHESION]
                       ]
        return google_item
