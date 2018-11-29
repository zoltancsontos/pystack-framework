import os
import mimetypes
from helpers.general_helpers import GeneralHelpers
from settings.settings import SETTINGS


class BaseAsset(object):
    """
    Handles static assets
    """

    content_type = ''
    routes = []

    def __init__(self, storage_path):
        """
        Constructor
        Args:
            storage_path: string
        Returns:
        """
        self.storage_path = storage_path

    def on_get(self, req, resp, name):
        """
        Default HTTP GET handler
        Args:
            req: object
            resp: object
            name: object
        Returns:
        """
        content_type = mimetypes.guess_type(name)[0]
        resp.content_type = content_type if content_type is not None else 'application/octet-stream'
        file_path = os.path.join(self.storage_path, name)
        resp.stream = open(file_path, 'rb')
        resp.stream_len = os.path.getsize(file_path)

assets_path = SETTINGS['ASSETS_PATH']
assets_dir_paths = GeneralHelpers.get_dir_structure(assets_path)
asset_routes = []

for asset_route in assets_dir_paths:
    parsed_asset_route = asset_route['url'].replace('\\', '/')
    asset_routes.append({
        'url': parsed_asset_route + "/{name}",
        'controller': BaseAsset(asset_route['path'])
    })
