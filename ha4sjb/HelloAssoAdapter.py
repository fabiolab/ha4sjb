from loguru import logger
import pendulum

LABEL_EXTERIEUR = "Extérieur"
LABEL_LICENCIE = "Licencié"
LABEL_OUI = "Oui"
LABEL_NON = "Non"
LABEL_FAIT = "Fait"
LABEL_A_FAIRE = "A faire"
LABEL_HELLOASSO = "HelloAsso"


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

        creneau = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Créneau')
        if creneau is None:
            creneau = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Créneau jeune')

        facture = HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Facture')
        if facture == LABEL_OUI:
            facture = LABEL_A_FAIRE

        poona = LABEL_NON
        if item['option_label'] == "Extérieur":
            poona = "Extérieur"

        # The order must match the GoogleSheet columns
        google_item = [
            item['id'],
            pendulum.parse(item['date']).format('DD/MM/YYYY'),
            now.format('DD/MM/YYYY'),
            item['last_name'].upper(),
            item['first_name'],
            HelloAssoAdapter.get_custom_value(item['custom_infos'], 'Genre'),
            pendulum.parse(HelloAssoAdapter.get_custom_value(item['custom_infos'],
                                                             'Date de naissance')).format('DD/MM/YYYY'),
            None,
            creneau,
            LABEL_EXTERIEUR if item['option_label'] == LABEL_EXTERIEUR else LABEL_LICENCIE,
            LABEL_OUI,
            HelloAssoAdapter.get_custom_value(item['custom_infos'], "Autorisation mineurs"),
            HelloAssoAdapter.get_custom_value(item['custom_infos'],
                                              "Certificat médical de moins d'un an ou Questionnaire Santé"),
            None,
            poona,
            facture,
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
