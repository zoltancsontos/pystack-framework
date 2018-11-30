from falcon_multipart.middleware import MultipartMiddleware
from middlewares.Error_middleware import ErrorMiddleware
from middlewares.Authentication_middleware import AuthenticationMiddleware
from middlewares.Ssl_middleware import SslMiddleware

# Put any application level middlewares here
middlewares = [
    SslMiddleware(),
    MultipartMiddleware(),
    ErrorMiddleware(),
    AuthenticationMiddleware()
]
