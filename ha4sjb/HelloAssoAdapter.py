from loguru import logger
import pendulum

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

    def load_from_apiresponse(self, resources: list):
        google_items = list()
        for item in resources:
            google_items.append(self.h4_to_google(item))

        logger.info(f"{len(google_items)} items loaded")
        return google_items

    @staticmethod
    def get_custom_value(custom_values: list, searched_key: str) -> str:
        for element in custom_values:
            if element['label'] == searched_key:
                return element['value']

        return None

    @staticmethod
    def h4_to_google(item: dict) -> list:
        now = pendulum.now()

        google_item = [item['date'],
                       now.format('DD/MM/YYYY'),
                       item['last_name'].upper(),
                       item['first_name'],
                       HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Genre'),
                       HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Date de naissance'),
                       None,
                       MATCH_CRENEAUX.get(HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Créneau')),
                       LABEL_EXTERIEUR if item['option_label'] == LABEL_EXTERIEUR else LABEL_LICENCIE,
                       LABEL_OUI,
                       HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Certificat médical'),
                       LABEL_NON,
                       HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Questionnaire Santé Sport'),
                       LABEL_FAIT,
                       HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Interclubs'),
                       item['email'],
                       HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Code Postal'),
                       LABEL_OUI,
                       None,
                       LABEL_HELLOASSO,
                       None,
                       None,
                       None,
                       f"{item['amount']} €"
                       ]
        return google_item
