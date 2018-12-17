from core.base_model import *


class TodosModel(BaseModel):
    """
    Todos model definition
    :notes: add any additional fields below id
    """
    id = AutoField()
    name = CharField()
    status = CharField()

    class Meta:
        order_by = ('id',)
        table_name = 'todos'
