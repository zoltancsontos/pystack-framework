from modules.Users.Users_resource import UsersResource
from modules.Users.LoginService_resource import LoginService
from modules.Users.RegistrationService_resource import RegistrationService
from modules.Users.LogoutService_resource import LogoutService

routes = [
    # Users api routes
    {'url': '/v1/users', 'controller': UsersResource()},
    {'url': '/v1/users/{uid}', 'controller': UsersResource()},
    {'url': '/v1/users/login', 'controller': LoginService()},
    {'url': '/v1/users/register', 'controller': RegistrationService()},
    {'url': '/v1/users/logout', 'controller': LogoutService()}
]
