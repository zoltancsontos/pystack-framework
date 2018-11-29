from core.base_resource import BaseResource
from modules.Users.Users_model import UsersModel


class UsersResource(BaseResource):
    """
    Users resource handler
    """
    model = UsersModel
    property_types = []
    allowed_methods = ['GET']
    transient_properties = ['password']

