from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.UserToken_model import UserTokenModel
from core.sys_modules.authentication.UsersPermissions_model import UsersPermissionsModel
import hashlib
import jwt
import datetime
from settings.settings import SETTINGS
from core.base_resource import BaseResource


class UserServices:
    """
    User services
    """
    model = UsersModel
    permissions_model = UsersPermissionsModel
    __secret__ = SETTINGS['AUTHENTICATION']['SECRET']
    __expiration_hours__ = SETTINGS['AUTHENTICATION']['EXPIRATION_HOURS']

    @staticmethod
    def login(login, password):
        if login and password is not None:
            encoded_password = hashlib.sha3_512(password.encode('utf-8')).hexdigest()
            try:
                user = UserServices.model.get(
                    UsersModel.email == login,
                    UsersModel.password == encoded_password
                )
                raw_data = UserServices.permissions_model().select().where(UsersPermissionsModel.user == user.id)
                user_permissions = []
                if raw_data:
                    for data in raw_data:
                        user_permissions.append({
                            'group_id': data.group.id,
                            'group_name': data.group.group_name
                        })
            except UserServices.model.DoesNotExist:
                user = None
                user_permissions = None
            if user is not None:
                payload = {
                    'payload': {
                        'user_id': user.id,
                        'user_login': user.email,
                        'permissions': user_permissions
                    },
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=UserServices.__expiration_hours__)
                }
                token = jwt.encode(payload, UserServices.__secret__, algorithm='HS256')
                token_data = {
                    "token": token,
                    "user": user
                }
                existing_token = UserTokenModel().select().where(UserTokenModel.user == user).first()
                if existing_token:
                    UserTokenModel().delete_by_id(existing_token.id)
                UserTokenModel().add(token_data)
                BaseResource().conn.close()
                return token
        BaseResource.conn.close()
        return None

    @staticmethod
    def logout(token):
        stored_token = UserTokenModel().select().where(UserTokenModel.token == token).first()
        if stored_token:
            UserTokenModel().delete_by_id(stored_token.id)
        BaseResource().conn.close()

    @staticmethod
    def validate(token):
        """
        Validates the token
        :param token:
        :return:
        """
        existing_token = UserTokenModel().select().where(UserTokenModel.token == token).first()
        if existing_token:
            try:
                jwt.decode(token, UserServices.__secret__, algorithm='HS256')
                BaseResource().conn.close()
                return True
            except jwt.ExpiredSignatureError or jwt.InvalidTokenError or jwt.InvalidSignatureError:
                UserTokenModel().delete_by_id(existing_token.id)
                BaseResource().conn.close()
                return False
        BaseResource().conn.close()
        return False

    @staticmethod
    def get_data_from_token(token):
        try:
            BaseResource.conn.close()
            return jwt.decode(token, UserServices.__secret__, algorithm='HS256')
        except jwt.ExpiredSignatureError or jwt.InvalidTokenError or jwt.InvalidSignatureError:
            BaseResource.conn.close()
            return {}
