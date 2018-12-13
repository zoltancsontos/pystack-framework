from core.base_resource import BaseResource
from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.UsersPermissions_model import UsersPermissionsModel
from core.sys_modules.authentication.PermissionGroups_model import PermissionGroupsModel
from core.sys_modules.authentication.UserServices import UserServices
from falcon import falcon
import json
import hashlib


class UpdateService(BaseResource):
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
    }, {
        'key': 'permissions',
        'type': list,
        'required': False
    }]
    allowed_methods = ['PUT']

    @falcon.after(BaseResource.conn.close)
    def on_put(self, req, resp, uid=None):
        """
        Main registration method
        :param req: object
        :param resp: object
        :param uid: number
        :return:
        """
        req_body = req.stream.read().decode('utf-8')
        content = json.loads(req_body, encoding='utf-8')
        token = req.cookies['token']
        user_id, user_login, permissions = UpdateService.__extract_token_data__(token)
        permission_strings = [perm['group_name'] for perm in permissions]
        int_uid = int(uid)

        if self.__has_mandatory_props__(content, resp):

            try:
                current_data = self.model.get(UsersModel.id == uid)
            except self.model.DoesNotExist:
                current_data = None

            if current_data:
                if not self.__check_if_username_used__(content['email'], int_uid):
                    if current_data.id == int_uid or 'ADMIN' in permission_strings:
                        if 'permissions' in content and 'ADMIN' in permission_strings:
                            permission_data = content['permissions']
                            self.__update_permissions__(permission_data, user_id, int_uid)
                            del content['permissions']

                        encoded_pwd = hashlib.sha3_512(content['password'].encode('utf-8')).hexdigest()
                        content['password'] = encoded_pwd
                        self.model().change(content, self.model, uid)

                        try:
                            db_data = self.permissions_model.select()\
                                .join(PermissionGroupsModel, on=(PermissionGroupsModel.id == UsersPermissionsModel.id))\
                                .where(UsersPermissionsModel.user == int_uid)
                        except self.permissions_model.DoesNotExist:
                            db_data = None

                        del content['password']
                        data = {
                            'permissions': [item.group.group_name for item in db_data],
                            'user_details': content
                        }

                        resp.content_type = "application/json"
                        resp.status = falcon.HTTP_200
                        resp.body = (json.dumps(data))
                        BaseResource.conn.close()
                        return
                    else:
                        self.__raise_exception__('unauthorized', 'Unauthorized', 'trying to access a resource '
                                                                                 'that doesn\'t belong to you')
                else:
                    self.__raise_exception__('bad_req', 'Email already used', 'Please use a different email...')
            self.__raise_exception__('bad_req', 'Non existing user', 'There\'s no user with id: {}'.format(uid))
        self.__raise_exception__('bad_req', 'Bad request', 'Missing mandatory request property...')

    @staticmethod
    def __raise_exception__(exc_type, title, message):
        BaseResource.conn.close()
        if exc_type == 'unauthorized':
            raise falcon.HTTPUnauthorized('Unauthorized', 'trying to access a resource'
                                                          ' that doesn\'t belong to you')
        else:
            raise falcon.HTTPBadRequest(title, message)

    def __update_permissions__(self, permission_data, user_id, int_uid):
        """
        Updates the permissions if the user is admin
        :param permission_data: list
        :param user_id: int
        :param int_uid: int
        :return:
        """
        if user_id != int_uid:
            q = self.permissions_model().delete().where(UsersPermissionsModel.user == int_uid)
            q.execute()
            for permission in permission_data:
                permission_id = self.permission_groups_model().get(PermissionGroupsModel.group_name == permission)
                insert_data = {
                    'user': int_uid,
                    'group': permission_id
                }
                self.permissions_model().add(insert_data)

    @staticmethod
    def __extract_token_data__(token):
        """
        Extracts the token data
        :param token:
        :return:
        """
        token_data = UserServices.get_data_from_token(token)
        user_id, user_login, permissions = token_data['payload'].values()
        return user_id, user_login, permissions

    def __check_if_username_used__(self, user_name, uid):
        """
        Checks if the username already exists
        :param user_name: str
        :param uid: int
        :return: boolean
        """
        user = self.model.select().where(self.model.email == user_name, self.model.id != uid)
        if user.exists():
            return True
        return False
