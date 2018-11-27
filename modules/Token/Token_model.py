from core.base_model import *
from modules.Users.Users_model import UsersModel
import datetime


class TokenModel(BaseModel):
    """
    Token model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    user = ForeignKeyField(UsersModel, backref="tokens")
    token = CharField(max_length=240)
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('id',)
        table_name = "token_model"
