import os
from core.orm.db_type import DbType

env = os.environ

"""
Generic application SETTINGS
"""
SETTINGS = {
    'APP_VERSION': 'v1',
    'APP_NAME': 'PyStack',
    'DATABASE': {
        'ADAPTER_TYPE': DbType.SQLLITE,
        'SQL_DEBUG': True
    },
    'AUTHENTICATION': {
        'ENABLE_SYS_AUTHENTICATION': True,
        'SECRET': 'as63518s*&6291sjcbsja',
        'EXPIRATION_HOURS': 24
    },
    'VIEWS': {
        'DEFAULT_TEMPLATES_DIR': 'templates',
        'DEFAULT_LOGIN_PAGE_TEMPLATE': 'Login_page.html',
        'DEFAULT_404_TEMPLATE': '404.html',
        'DEFAULT_401_TEMPLATE': '401.html'
    },
    'ASSETS_PATH': 'front-end',
    'SECURE_COOKIES': False,
    'PERMISSIONS': {
        'GROUPS': [
            'ADMIN',
            'USER',
            'EDITOR',
            'DEVELOPER'
        ],
        'DEFAULT_GROUP': 'USER'
    },
    'DEFAULT_ADMIN_EMAIL': 'admin@admin.com',
    'DEFAULT_ADMIN_PASSWORD': 'admin',
    'FORCE_SSL': True,
    'SWAGGER_CONFIG': {
        'ENABLED': True,
        'DOCUMENTATION_TITLE': 'App title',
        'DOCUMENTATION_DESCRIPTION': 'Api documentation',
        'TERMS_AND_CONDITIONS_URL': 'http://www.google.com'
    },
    'CORS': {
        'ALLOWED_ORIGINS': 'http://localhost:3000',
        'ALLOWED_METHODS': 'GET, PUT, POST, DELETE, OPTIONS, PATCH',
        'ALLOWED_HEADERS': 'Content-Type, Bearer, Authorization',
        'ALLOW_CREDENTIALS': True
    }
}
