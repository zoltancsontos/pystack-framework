from core.sys_modules.swagger.Swagger_page import SwaggerPage
from core.sys_modules.swagger.SwaggerConfiguration_generator import SwaggerConfigurationGenerator
from settings.settings import SETTINGS

app_version = SETTINGS['APP_VERSION']

if SETTINGS['SWAGGER_CONFIG']['ENABLED']:
    routes = [
        # swagger page routes
        {'url': '/{}/swagger-ui'.format(app_version), 'controller': SwaggerPage()},
        {'url': '/{}/swagger-config'.format(app_version), 'controller': SwaggerConfigurationGenerator()}
    ]
