import os
import re

env = os.environ

"""
Generic application SETTINGS
"""


def __get_connection_parts__():
    conn_str = env['CLEARDB_DATABASE_URL']
    user, password, host, database = re.match('mysql://(.*?):(.*?)@(.*?)/(.*)', conn_str).groups()
    return user, password, host, database


db_user, db_password, db_host, db_schema = __get_connection_parts__()

SETTINGS = {
    'DATABASE': {
        'CONNECTION_STRING': env['CLEARDB_DATABASE_URL'],
        'HOST': db_host,
        'USER': db_user,
        'PASSWORD': db_password,
        'PORT': 3306,
        'SCHEMA': db_schema
    },
    'AUTHENTICATION': {
        'SECRET': 'as63518s*&6291sjcbsja',
        'EXPIRATION_HOURS': 24
    },
    'VIEWS': {
        'DEFAULT_TEMPLATES_DIR': 'templates',
        'DEFAULT_404_TEMPLATE': '404.html'
    },
    'ASSETS_PATH': 'front-end',
    'SECURE_COOKIES': False
}
