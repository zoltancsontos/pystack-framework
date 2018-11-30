from falcon import falcon
from settings.settings import SETTINGS
import logging


class SslMiddleware(object):
    """
    Ssl forcing middleware
    """
    EXTENSION_WHITELIST = [
        '.css',
        '.js',
        '.png',
        '.svg',
        '.jpg',
        '.ico',
        '.map'
    ]

    def process_request(self, req, resp):
        for item in self.EXTENSION_WHITELIST:
            if SETTINGS['FORCE_SSL'] and item not in req.url:
                print('ssl is here', req.url)
                print(req.scheme)
                if 'https' not in req.url:
                    print('http')
                    new_url = req.url.replace('http', 'https')
                    logging.debug(new_url)
                    raise falcon.HTTPTemporaryRedirect(new_url)
