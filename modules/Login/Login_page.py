from core.base_page import BasePage


class LoginPage(BasePage):
    """
    LoginPage logic
    """
    templates_dir = "modules/Login/"
    template = "Login_template.html"

    def get_data(self, req):
        """
        Set up the data source
        Args:
            req: object
        Returns:
        """
        data = {
            "title": "Pysaw Login",
            "text": "Please log in"
        }
        return data
