from modules.Swagger.Swagger_page import SwaggerPage
from modules.Swagger.SwaggerConfig_handler import SwaggerConfigHandler
from modules.Swagger.SwaggerConfiguration_generator import SwaggerConfigurationGenerator
from settings.settings import SETTINGS

if SETTINGS['SWAGGER_CONFIG']['ENABLED']:
    routes = [
        # Swagger page routes
        {'url': '/v1/swagger-ui', 'controller': SwaggerPage()},
        {'url': '/v1/swagger-config', 'controller': SwaggerConfigHandler()},
        {'url': '/v2/swagger-config', 'controller': SwaggerConfigurationGenerator()}
    ]
