from falcon import falcon
from settings.settings import SETTINGS


class CorsMiddleware(object):
    """
    Cors middleware functionality
    """

    def process_request(self, req, resp):
        """
        Allows cors depending on settings
        :param req:
        :param resp:
        :return:
        """
        cors_settings = SETTINGS['CORS']
        resp.set_header('Access-Control-Allow-Origin', cors_settings['ALLOWED_ORIGINS'])
        resp.set_header('Access-Control-Allow-Methods', cors_settings['ALLOWED_METHODS'])
        resp.set_header('Access-Control-Allow-Headers', cors_settings['ALLOWED_HEADERS'])
        resp.set_header('Access-Control-Max-Age', 1728000)
        if cors_settings['ALLOW_CREDENTIALS']:
            resp.set_header('Access-Control-Allow-Credentials', 'true')
        if req.method == 'OPTIONS':
            raise falcon.HTTPStatus(falcon.HTTP_200, body='\n')
