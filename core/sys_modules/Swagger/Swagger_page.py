from core.base_page import BasePage


class SwaggerPage(BasePage):
    """
    SwaggerPage logic
    """
    templates_dir = "core/sys_modules/Swagger/"
    template = "Swagger_template.html"
    group_access = ['ADMIN', 'DEVELOPER']

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
