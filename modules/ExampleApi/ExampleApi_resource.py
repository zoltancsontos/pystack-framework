from core.base_resource import BaseResource
from modules.ExampleApi.ExampleApi_model import ExampleApiModel


class ExampleApiResource(BaseResource):
    """
    ExampleApi resource handler
    """
    model = ExampleApiModel
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
