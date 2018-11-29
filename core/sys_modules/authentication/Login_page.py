from core.base_page import BasePage


class LoginPage(BasePage):
    """
    LoginPage logic
    """
    templates_dir = "templates/"
    template = "Login_page.html"

    def get_data(self, req):
        """
        Set up the data source
        Args:
            req: object
        Returns:
        """
        data = {
            "title": "PyStack Login",
            "text": "Please log in"
        }
        return data
