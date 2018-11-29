import falcon
from core.db_adapter import mysql_adapter
from core.base_model import database_proxy
from settings.settings import SETTINGS
from settings.routes import routes
from settings.mapped_models import MAPPED_MODELS
from settings.middlewares import middlewares
import logging

# log all peewee queries
if SETTINGS['DATABASE']['SQL_DEBUG']:
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

# Initialize the ORM
adapter = mysql_adapter
adapter.connect()
database_proxy.initialize(adapter.db_instance)

# Create the ORM models if already not exists
if database_proxy.obj is not None:
    adapter.create_tables(MAPPED_MODELS)

# Close the database adapter
adapter.close()

# Declare the falcon application
app = falcon.API(middleware=middlewares)
app.resp_options.secure_cookies_by_default = SETTINGS['SECURE_COOKIES']

# route mappings
for route in routes:
    app.add_route(route['url'], route['controller'])
