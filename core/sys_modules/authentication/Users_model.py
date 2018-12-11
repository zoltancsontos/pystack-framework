from core.base_model import *
from settings.settings import SETTINGS
import hashlib
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

    initial_data = [{
        'first_name': 'admin',
        'middle_name': '',
        'last_name': 'admin',
        'email': SETTINGS['DEFAULT_ADMIN_EMAIL'],
        'password': hashlib.sha3_512(SETTINGS['DEFAULT_ADMIN_PASSWORD'].encode('utf-8')).hexdigest()
    }]

    class Meta:
        order_by = ('id',)
        table_name = "sys_users"
