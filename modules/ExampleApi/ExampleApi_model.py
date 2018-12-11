from core.base_model import *


class ExampleApiModel(BaseModel):
    """
    ExampleApi model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()
    item_name = CharField()
    item_type = CharField()

    class Meta:
        order_by = ('id',)
        table_name = 'example_api'
