from core.base_resource import BaseResource
from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.UsersPermissions_model import UsersPermissionsModel
from core.sys_modules.authentication.PermissionGroups_model import PermissionGroupsModel
from settings.settings import SETTINGS
from falcon import falcon
import json
import hashlib


class RegistrationService(BaseResource):
    """
    Registration service
    """
    model = UsersModel
    permissions_model = UsersPermissionsModel
    permission_groups_model = PermissionGroupsModel

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
        default_group = SETTINGS['PERMISSIONS']['DEFAULT_GROUP']
        req_body = req.stream.read().decode('utf-8')
        content = json.loads(req_body, encoding='utf-8')
        if self.__has_mandatory_props__(content, resp):
            if not self.__check_if_username_used__(content['email'], resp):
                encoded_pwd = hashlib.sha3_512(content['password'].encode('utf-8')).hexdigest()
                content['password'] = encoded_pwd

                last_id = self.model().add(content)
                content['id'] = last_id
                del content['password']

                try:
                    stored_permission = self.permission_groups_model.get(PermissionGroupsModel.group_name == default_group)
                except self.permission_groups_model.DoesNotExist:
                    stored_permission = None
                if stored_permission is not None:
                    permission_data = {
                        "user":  last_id,
                        "group": stored_permission.id
                    }
                    self.permissions_model().add(permission_data)

                resp.content_type = "application/json"
                resp.status = falcon.HTTP_201
                resp.body = (json.dumps(content))
            else:
                raise falcon.HTTPBadRequest("Bad request", "user already exists")

    def __check_if_username_used__(self, user_name: str, resp):
        """
        Checks if the username already exists
        :param user_name: str
        :param resp: object
        :return: boolean
        """
        user = self.model.select().where(self.model.email == user_name)
        if user.exists():
            return True
        return False
