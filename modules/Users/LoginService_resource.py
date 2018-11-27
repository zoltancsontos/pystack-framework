from core.base_resource import BaseResource
from modules.Users.Users_model import UsersModel
from modules.Users.UserServices import UserServices
from falcon import *
import json


class LoginService(BaseResource):
    """
    Login service
    """
    model = UsersModel
    property_types = []
    allowed_methods = ['POST']

    @falcon.after(BaseResource.conn.close)
    def on_post(self, req, resp):
        req_body = req.stream.read().decode('utf-8')
        req_data = json.loads(req_body, encoding='utf-8')
        resp.content_type = "application/json"

        resp_status = falcon.HTTP_400
        body = {
            'message': 'Missing mandatory parameters login or password'
        }
        if 'login' and 'password' in req_data:
            login = req_data['login']
            password = req_data['password']
            token = UserServices.login(login, password)
            if token is not None:
                resp.status = falcon.HTTP_200
                resp.set_cookie("token", str(token, encoding="utf-8"))
                resp.body = (json.dumps({
                    "token": token
                }, indent=4, sort_keys=True, default=str))
                return
            resp_status = falcon.HTTP_401
            body = {
                'message': 'Bad login or password, or non-existing user'
            }

        resp.status = resp_status
        resp.body = (json.dumps(body))
