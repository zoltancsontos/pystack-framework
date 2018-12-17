from core.base_resource import BaseResource
from modules.Todos.Todos_model import TodosModel


class TodosResource(BaseResource):
    """
    Todos resource handler
    """
    model = TodosModel
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
