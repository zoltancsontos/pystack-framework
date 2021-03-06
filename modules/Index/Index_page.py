from core.base_page import BasePage


class IndexPage(BasePage):
    """
    BasePage test
    """
    templates_dir = "modules/Index/"
    template = "Index_template.html"

    def get_data(self, req):
        """
        Set up the data source
        Args:
            req: object
        Returns:
        """
        data = {
            "title": "PyStack framework",
            "text": "Welcome to PyStack framework!"
        }
        return data
