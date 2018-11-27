from core.base_model import *
import datetime


class SettingsModel(BaseModel):
    """
    Settings model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    site_name = CharField()
    site_description = CharField()
    last_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('id',)
