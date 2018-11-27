from helpers.general_helpers import GeneralHelpers
from core.assets_handler import asset_routes

routes = [] + GeneralHelpers.get_app_routes() + asset_routes
