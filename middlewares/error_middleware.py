from falcon import *
from settings.settings import *
from settings.routes import routes

from chameleon import PageTemplateLoader


class ErrorMiddleware(object):
    """
    Error handling middleware
    """

    @staticmethod
    def __load_error_template__(template_type='DEFAULT_404_TEMPLATE'):
        """
        Loads the specified templates
        Args:
            template_type: string
        Returns:
        """
        base_dir_path = SETTINGS['VIEWS']['DEFAULT_TEMPLATES_DIR']
        app_path = os.path.abspath(base_dir_path)
        templates = PageTemplateLoader(app_path)
        template = templates[SETTINGS['VIEWS'][template_type]]
        return template

    @staticmethod
    def __check_if_route_exists(route):
        """
        Check if route exists in the URL map
        Args:
            route:
        Returns: boolean
        """
        found = True
        for app_route in routes:
            if route not in app_route['url'] \
                    and 'assets' not in route \
                    and 'build' not in route \
                    and 'doc' not in route:
                found = False
                break
        return found

    def process_request(self, req, resp):
        """
        Args:
            req:
            resp:
        Returns:
        """
        route = req.relative_uri
        if not self.__check_if_route_exists(route):
            template = self.__load_error_template__()
            resp.status = falcon.HTTP_404
            resp.content_type = "text/html"
            resp.body = (template(data=req))
