from core.base_resource import BaseResource
from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.UserServices import UserServices
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
        req_content_type = "" if req.content_type is None else req.content_type
        cookies = req.cookies
        token = ""
        if 'token' in cookies:
            token = cookies['token']

        resp.content_type = "application/json"
        resp.status = falcon.HTTP_200
        resp.unset_cookie("token")

        if token is not None:
            UserServices.logout(token)

        if 'json' in req_content_type:
            resp.body = (json.dumps({
                'message': 'You were successfully logged out'
            }, indent=4, sort_keys=True, default=str))
        else:
            raise falcon.HTTPTemporaryRedirect("/login")
