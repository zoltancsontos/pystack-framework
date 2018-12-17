from falcon_multipart.middleware import MultipartMiddleware
from middlewares.Error_middleware import ErrorMiddleware
from middlewares.Authentication_middleware import AuthenticationMiddleware
from middlewares.Cors_middleware import CorsMiddleware

# Put any application level middlewares here
middlewares = [
    MultipartMiddleware(),
    ErrorMiddleware(),
    AuthenticationMiddleware(),
    CorsMiddleware()
]
