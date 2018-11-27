from core.base_resource import BaseResource
from modules.Settings.Settings_model import SettingsModel


class SettingsResource(BaseResource):
    """
    Settings resource handler
    """
    model = SettingsModel
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
