from enum import Enum


class DbType(Enum):
    """
    Connection type enumerator
    """
    MYSQL = 1
    POSTGRES = 2
    SQLLITE = 3
