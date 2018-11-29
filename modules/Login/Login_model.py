from core.base_model import *


class LoginModel(BaseModel):
    """
    Login model definition
    :notes: add any additional fields below id
    """
    id = PrimaryKeyField()

    class Meta:
        order_by = ('id',)
