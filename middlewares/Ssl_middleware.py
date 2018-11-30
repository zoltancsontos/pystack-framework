from falcon import falcon
from settings.settings import SETTINGS
import logging


class SslMiddleware(object):
    """
    Ssl forcing middleware
    """

    def process_request(self, req, resp):
        if SETTINGS['FORCE_SSL']:
            print('ssl is here', req.url)
            print(req.scheme)
            if 'https' not in req.url:
                print('http')
                new_url = req.url.replace('http', 'https')
                logging.debug(new_url)
                raise falcon.HTTPTemporaryRedirect(new_url)
