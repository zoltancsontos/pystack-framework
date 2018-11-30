from settings.settings import SETTINGS
from core.sys_modules.authentication.Login_page import LoginPage
from core.sys_modules.authentication.AccessDenied_page import AccessDeniedPage
from core.sys_modules.authentication.LoginService_resource import LoginService
from core.sys_modules.authentication.RegistrationService_resource import RegistrationService
from core.sys_modules.authentication.LogoutService_resource import LogoutService
from core.sys_modules.authentication.Users_resource import UsersResource

auth_settings = SETTINGS['AUTHENTICATION']['ENABLE_SYS_AUTHENTICATION']
app_version = SETTINGS['APP_VERSION']

if auth_settings is True:
    routes = [
        # System users api routes
        {'url': '/login', 'controller': LoginPage()},
        {'url': '/{}/users/user-info'.format(app_version), 'controller': UsersResource()},
        {'url': '/{}/users/login'.format(app_version), 'controller': LoginService()},
        {'url': '/{}/users/register'.format(app_version), 'controller': RegistrationService()},
        {'url': '/{}/users/logout'.format(app_version), 'controller': LogoutService()},
        {'url': '/access-denied'.format(app_version), 'controller': AccessDeniedPage()}
    ]
