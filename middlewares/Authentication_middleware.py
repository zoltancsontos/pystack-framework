from falcon import falcon
from core.sys_modules.authentication.UserServices import UserServices
from core.base_resource import BaseResource
from settings.settings import SETTINGS


class AuthenticationMiddleware(object):
    """
    Authentication middleware class
    """

    URL_WHITE_LIST = [
        '/v1/users/logout',
        '/v1/users/login',
        '/v1/users/register',
        '/login'
    ]

    EXTENSION_WHITELIST = [
        '.css',
        '.js',
        '.png',
        '.svg',
        '.jpg',
        '.ico'
    ]

    def process_request(self, req, resp):
        """
        Args:
            req:
            resp:
        Returns:
        """
        if SETTINGS['AUTHENTICATION']['ENABLE_SYS_AUTHENTICATION'] is True:
            url = req.relative_uri
            is_file = False

            for ext in self.EXTENSION_WHITELIST:
                if ext in url:
                    is_file = True
                    break

            if url not in self.URL_WHITE_LIST and not is_file:
                content_type = '' if req.content_type is None else req.content_type
                cookies = req.cookies
                valid = False
                if 'token' in cookies:
                    token = cookies['token']
                    valid = UserServices.validate(token)

                if not valid:
                    if 'json' in content_type:
                        resp.status = falcon.HTTP_404
                        resp.content_type = 'application/json'
                        resp.unset_cookie('token')
                        raise falcon.HTTPUnauthorized('Access denied', 'in order to continue please log in')
                    else:
                        redirect = req.relative_uri
                        resp.unset_cookie('redirect')
                        if 'logout' not in redirect:
                            resp.set_cookie('redirect', redirect.strip('\"'), max_age=600, path='/', http_only=False)
                        raise falcon.HTTPTemporaryRedirect('/login')

    @falcon.after(BaseResource.conn.close)
    def process_response(self, req, resp):
        """
        Close the db connection after the request is processed
        :param req:
        :param resp:
        :return:
        """
        pass
