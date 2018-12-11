from core.base_model import *
from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.PermissionGroups_model import PermissionGroupsModel


class UsersPermissionsModel(BaseModel):
    """
    Users model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    user = ForeignKeyField(UsersModel, backref="user")
    group = ForeignKeyField(PermissionGroupsModel, backref="permission")
    initial_data = [{
        'user': 1,
        'group': 1
    }]

    class Meta:
        order_by = ('id',)
        table_name = "sys_users_permissions"
