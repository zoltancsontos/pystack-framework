import os
from falcon import falcon
from settings.settings import SETTINGS

from chameleon import PageTemplateLoader


class BasePage(object):
    """
    Generic base page object
    """

    model = None
    property_types = []
    default_404 = SETTINGS['VIEWS']['DEFAULT_404_TEMPLATE']
    templates_dir = 'templates/'
    template = 'index.html'
    data = {}
    allowed_methods = ['GET']
    group_access = SETTINGS['PERMISSIONS']['GROUPS']

    def load_templates(self, base_dir=None):
        """
        Loads the specified templates
        Args:
            base_dir: string|None
        Returns:
        """
        base_dir_path = base_dir if base_dir else self.templates_dir
        app_path = os.path.abspath(base_dir_path)
        return PageTemplateLoader(app_path)

    def get_data(self, req):
        """
        Method to override for data retrieval
        Args:
            req: object
        Returns: mixed
        """
        return self.data

    def __forbidden_handler__(self, req, resp):
        """
        Default forbidden case handler.
        Explanation: As this is the BasePage super class
        anything except GET should be forbidden you should use
        BaseResource instead of page and create a proper REST api
        Args:
            req:
            resp:
        Returns:
        """
        templates = self.load_templates(base_dir="/templates")
        template = templates[self.default_404]
        resp.status = falcon.HTTP_404
        resp.content_type = "text/html"
        data = {
            'req': req
        }
        resp.body = (template(data=data))

    def on_get(self, req, resp):
        """
        Default HTTP GET method definition
        Args:
            req: object
            resp: object
        Returns:
        """
        data = self.get_data(req)
        templates = self.load_templates()
        try:
            print(self.template)
            template = templates[self.template]
        except ValueError as val:
            self.__forbidden_handler__(req, resp)
        resp.status = falcon.HTTP_200
        resp.content_type = "text/html"
        resp.body = (template(data=data))

    def on_post(self, req, resp):
        """
        Default POST http method handler
        Args:
            req:
            resp:
        Returns:
        """
        self.__forbidden_handler__(req, resp)

    def on_put(self, req, resp):
        """
        Default PUT http method handler
        Args:
            req:
            resp:
        Returns:
        """
        self.__forbidden_handler__(req, resp)

    def on_delete(self, req, resp):
        """
        Default DELETE http method handler
        Args:
            req:
            resp:
        Returns:
        """
        self.__forbidden_handler__(req, resp)

    def on_patch(self, req, resp):
        """
        Default PATCH http method handler
        Args:
            req:
            resp:
        Returns:
        """
        self.__forbidden_handler__(req, resp)
