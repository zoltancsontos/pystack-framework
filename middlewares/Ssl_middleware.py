from falcon import falcon
from settings.settings import SETTINGS


class SslMiddleware(object):
    """
    Ssl forcing middleware
    """

    def process_request(self, req, resp):
        if SETTINGS['FORCE_SSL']:
            if req.scheme == 'http':
                new_url = req.url.replace('http', 'https')
                print(new_url)
                raise falcon.HTTPPermanentRedirect(new_url)
