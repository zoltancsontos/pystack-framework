from core.base_resource import BaseResource
from modules.Users.Users_model import UsersModel
from falcon import *
import json
import hashlib


class RegistrationService(BaseResource):
    """
    Registration service
    """
    model = UsersModel
    property_types = [{
        'key': 'first_name',
        'type': str,
        'required': True
    }, {
        'key': 'middle_name',
        'type': str,
        'required': False
    }, {
        'key': 'last_name',
        'type': str,
        'required': True
    }, {
        'key': 'email',
        'type': str,
        'required': True
    }, {
        'key': 'password',
        'type': str,
        'required': True
    }]
    allowed_methods = ['POST']

    @falcon.after(BaseResource.conn.close)
    def on_post(self, req, resp):
        """
        Main registration method
        :param req: object
        :param resp: object
        :return:
        """
        req_body = req.stream.read().decode('utf-8')
        content = json.loads(req_body, encoding='utf-8')
        if self.__has_mandatory_props__(content, resp):
            if not self.__check_if_username_used__(content['email'], resp):
                encoded_pwd = hashlib.sha3_512(content['password'].encode('utf-8')).hexdigest()
                content['password'] = encoded_pwd
                last_id = self.model().add(content)
                content['id'] = last_id
                del content['password']
                resp.content_type = "application/json"
                resp.status = falcon.HTTP_201
                resp.body = (json.dumps(content))

    def __check_if_username_used__(self, user_name: str, resp):
        """
        Checks if the username already exists
        :param user_name: str
        :param resp: object
        :return: boolean
        """
        user = self.model.select().where(self.model.email == user_name)
        if user.exists():
            resp.content_type = "application/json"
            resp.status = falcon.HTTP_400
            resp.body = (json.dumps({
                "message": "user with the provided email already exists"
            }))
            return True
        return False
