from falcon import falcon
from settings.settings import SETTINGS
import logging


class SslMiddleware(object):
    """
    Ssl forcing middleware
    """

    def process_request(self, req, resp):
        if SETTINGS['FORCE_SSL']:
            print('ssl is here')
            if req.scheme == 'http':
                print('http')
                new_url = req.url.replace('http', 'https')
                logging.debug(new_url)
                raise falcon.HTTPTemporaryRedirect(new_url)
