from core.base_page import BasePage


class SwaggerPage(BasePage):
    """
    SwaggerPage logic
    """
    templates_dir = "modules/Swagger/"
    template = "Swagger_template.html"

    def get_data(self, req):
        """
        Set up the data source
        Args:
            req: object
        Returns:
        """
        data = {
            "title": "PyStack framework",
            "text": "Welcome to PyStack!"
        }
        return data