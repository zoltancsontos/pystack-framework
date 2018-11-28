from modules.Users.Users_model import UsersModel
from modules.Token.Token_model import TokenModel
import hashlib
import jwt
import datetime
from core.base_resource import BaseResource


class UserServices:
    """
    User services
    """
    model = UsersModel
    __secret__ = "as63518s*&6291sjcbsja"
    __expiration_hours__ = 24

    @staticmethod
    def login(login, password):
        if login and password is not None:
            encoded_password = hashlib.sha3_512(password.encode('utf-8')).hexdigest()
            user = UserServices.model.get(
                UserServices.model.email == login,
                UserServices.model.password == encoded_password
            )
            if user:
                payload = {
                    'payload': {
                        'user_id': user.id,
                        'user_login': user.email
                    },
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=UserServices.__expiration_hours__)
                }
                token = jwt.encode(payload, UserServices.__secret__, algorithm='HS256')
                token_data = {
                    "token": token,
                    "user": user
                }
                existing_token = TokenModel().select().where(TokenModel.user == user).first()
                if existing_token:
                    TokenModel().delete_by_id(existing_token.id)
                TokenModel().add(token_data)
                return token
        return None

    @staticmethod
    def logout(token):
        stored_token = TokenModel().select().where(TokenModel.token == token).first()
        if stored_token:
            TokenModel().delete_by_id(stored_token.id)

    @staticmethod
    def validate(token):
        """
        Validates the token
        :param token:
        :return:
        """
        existing_token = TokenModel().select().where(TokenModel.token == token).first()
        if existing_token:
            try:
                jwt.decode(token, UserServices.__secret__, algorithm='HS256')
                BaseResource().conn.close()
                return True
            except jwt.ExpiredSignatureError or jwt.InvalidTokenError or jwt.InvalidSignatureError:
                TokenModel().delete_by_id(existing_token.id)
                BaseResource().conn.close()
                return False
        BaseResource().conn.close()
        return False
