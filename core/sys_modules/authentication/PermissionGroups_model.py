from core.base_model import *
from settings.settings import SETTINGS


class PermissionGroupsModel(BaseModel):
    """
    Users model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    group_name = CharField(max_length=60)
    initial_data = [{"group_name": i} for i in SETTINGS['PERMISSIONS']['GROUPS']]

    class Meta:
        order_by = ('id',)
        table_name = "sys_permission_groups"
