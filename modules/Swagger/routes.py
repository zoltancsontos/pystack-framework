from modules.Swagger.Swagger_page import SwaggerPage
from modules.Swagger.SwaggerConfig_handler import SwaggerConfigHandler

routes = [
    # Swagger page routes
    {'url': '/v1/swagger-ui', 'controller': SwaggerPage()},
    {'url': '/v1/swagger-config', 'controller': SwaggerConfigHandler()}
]
