from core.base_resource import BaseResource
from modules.TimeSeries.TimeSeries_model import TimeSeriesModel


class TimeSeriesResource(BaseResource):
    """
    TimeSeries resource handler
    """
    model = TimeSeriesModel
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

