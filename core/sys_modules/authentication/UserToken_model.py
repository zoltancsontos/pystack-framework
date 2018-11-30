from core.base_model import *
from core.sys_modules.authentication.Users_model import UsersModel
import datetime


class UserTokenModel(BaseModel):
    """
    Token model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    user = ForeignKeyField(UsersModel, backref="tokens")
    token = TextField()
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('id',)
        table_name = "sys_user_tokens"
