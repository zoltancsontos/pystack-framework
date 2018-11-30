from core.base_page import BasePage
from settings.settings import SETTINGS


class AccessDeniedPage(BasePage):
    """
    Access denied page logic
    """
    templates_dir = "templates/"
    template = SETTINGS['VIEWS']['DEFAULT_401_TEMPLATE']

    def get_data(self, req):
        """
        Set up the data source
        Args:
            req: object
        Returns:
        """
        data = {
            "title": "PyStack",
            "text": "access denied"
        }
        return data
