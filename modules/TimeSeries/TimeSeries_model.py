from core.base_model import BaseModel, PrimaryKeyField, DateTimeField, FloatField
import datetime


class TimeSeriesModel(BaseModel):
    """
    TimeSeries model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    temperature = FloatField()
    time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('id',)
