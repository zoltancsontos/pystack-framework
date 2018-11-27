from falcon_multipart.middleware import MultipartMiddleware
from middlewares.error_middleware import ErrorMiddleware
from middlewares.authentication_middleware import AuthenticationMiddleware

# Put any application level middlewares here
middlewares = [
    MultipartMiddleware(),
    ErrorMiddleware(),
    AuthenticationMiddleware()
]
