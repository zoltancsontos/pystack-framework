from core.base_resource import BaseResource
from modules.Users.Users_model import UsersModel
from modules.Users.UserServices import UserServices
from falcon import *
import json


class LogoutService(BaseResource):
    """
    Login service
    """
    model = UsersModel
    property_types = []
    allowed_methods = ['GET']

    @falcon.after(BaseResource.conn.close)
    def on_get(self, req, resp, uid=0):
        cookies = req.cookies
        token = ""
        print(cookies)
        if 'token' in cookies:
            print(cookies['token'])
            token = cookies['token']

        resp.content_type = "application/json"
        resp.status = falcon.HTTP_200
        resp.unset_cookie("token")

        if token is not None:
            UserServices.logout(token)

        resp.body = (json.dumps({
            'message': 'You were successfully logged out'
        }, indent=4, sort_keys=True, default=str))
