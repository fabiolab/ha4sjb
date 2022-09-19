from loguru import logger
import urllib.parse
import pendulum

LABEL_EXTERIEUR = "Extérieur"
LABEL_LICENCIE = "Licencié"
LABEL_OUI = "Oui"
LABEL_NON = "Non"
LABEL_FAIT = "Fait"
LABEL_A_FAIRE = "A faire"
LABEL_AUTO = "Auto"
LABEL_HELLOASSO = "HelloAsso"

BASE_URL = 'https://www.helloasso.com/documents/documents_users_souscriptions/'


class HelloAssoAdapter:

    def __init__(self):
        self.items = list()

    def load_from_apiresponse(self, resources: list):
        google_items = list()
        for item in resources:
            if item['status'].upper() == "PROCESSED":
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

        creneau = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Créneau')
        if creneau is None:
            creneau = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Créneau jeune')

        facture = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Facture')
        if facture == LABEL_OUI:
            if int(item['amount']):
                facture = LABEL_AUTO
            else:
                facture = LABEL_A_FAIRE

        poona = LABEL_NON
        if item['option_label'] == "Extérieur":
            poona = "Extérieur"

        cp = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Code Postal')
        ville = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Ville').title()
        adresse = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Adresse').lower()

        # The order must match the GoogleSheet columns
        google_item = [
            item['id'],
            pendulum.parse(item['date']).format('DD/MM/YYYY'),
            now.format('DD/MM/YYYY'),
            item['last_name'].title(),
            item['first_name'].title(),
            HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Genre'),
            HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Date de naissance'),
            HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Lieu de naissance').title(),
            None,
            creneau,
            LABEL_EXTERIEUR if item['option_label'] == LABEL_EXTERIEUR else LABEL_LICENCIE,
            LABEL_OUI,
            HelloAssoAdapter.deal_url(HelloAssoAdapter.get_custom_value(item['custom_infos'], "Autorisation mineurs")),
            HelloAssoAdapter.deal_url(HelloAssoAdapter.get_custom_value(item['custom_infos'],
                                                                        "Certificat médical de moins d'un an ou Questionnaire Santé")),
            None,
            poona,
            facture,
            HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Interclubs'),
            item['email'],
            HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Numéro de téléphone'),
            adresse,
            ville,
            cp,
            None,
            LABEL_HELLOASSO,
            f"{item['amount']} €"
        ]

        return google_item

    @staticmethod
    def get_certificates(items_added):
        return [{'file_url': item[13], 'first_name': item[3], 'last_name': item[4]} for item in items_added]

    @staticmethod
    def deal_url(the_string: str) -> str:
        if not the_string:
            return the_string
        if the_string.lower().startswith('http'):
            return the_string
        return f"{BASE_URL}{urllib.parse.quote(the_string)}"
