from core.base_resource import BaseResource
from modules.Token.Token_model import TokenModel


class TokenResource(BaseResource):
    """
    Token resource handler
    """
    model = TokenModel
    """
    property_types are being used for validation - you could specify different rules for all model properties
    Example property type<Dictionary>:
    {
        'key': 'name of the model property',
        'type': 'expected type',
        'required': 'boolean'
    }
    """
    property_types = []
