from falcon import *
from modules.Users.UserServices import UserServices
from core.base_resource import BaseResource


class AuthenticationMiddleware(object):

    URL_WHITE_LIST = [
        '/v1/users/logout',
        '/v1/users/login',
        '/v1/users/register'
    ]

    """
    Authentication middleware class
    """
    def process_request(self, req, resp):
        """
        Args:
            req:
            resp:
        Returns:
        """
        url = req.relative_uri
        if url not in self.URL_WHITE_LIST:
            cookies = req.cookies
            valid = False
            if 'token' in cookies:
                token = cookies['token']
                valid = UserServices.validate(token)

            if not valid:
                resp.status = falcon.HTTP_404
                resp.content_type = "application/json"
                resp.unset_cookie("token")
                raise falcon.HTTPUnauthorized("Access denied", "in order to continue please log in")

    @falcon.after(BaseResource.conn.close)
    def process_response(self, req, resp):
        """
        Close the db connection after the request is processed
        :param req:
        :param resp:
        :return:
        """
        pass
