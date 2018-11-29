from core.base_model import *
import datetime


class UsersModel(BaseModel):
    """
    Users model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    first_name = CharField(max_length=60)
    middle_name = CharField(max_length=60)
    last_name = CharField(max_length=100)
    email = CharField(max_length=200)
    password = CharField(max_length=200)
    created = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('id',)
        table_name = "sys_users"
