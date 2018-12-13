from settings.settings import SETTINGS
from core.sys_modules.authentication.Login_page import LoginPage
from core.sys_modules.authentication.AccessDenied_page import AccessDeniedPage
from core.sys_modules.authentication.LoginService_resource import LoginService
from core.sys_modules.authentication.RegistrationService_resource import RegistrationService
from core.sys_modules.authentication.UpdateService_resource import UpdateService
from core.sys_modules.authentication.LogoutService_resource import LogoutService
from core.sys_modules.authentication.Users_resource import UsersResource

auth_settings = SETTINGS['AUTHENTICATION']['ENABLE_SYS_AUTHENTICATION']
app_version = SETTINGS['APP_VERSION']

if auth_settings is True:
    routes = [
        # System users api routes
        {'url': '/login', 'controller': LoginPage()},
        {'url': '/' + app_version + '/users/user-info', 'controller': UsersResource()},
        {'url': '/' + app_version + '/users/login', 'controller': LoginService()},
        {'url': '/' + app_version + '/users/register', 'controller': RegistrationService()},
        {'url': '/' + app_version + '/users/update/{uid}', 'controller': UpdateService()},
        {'url': '/' + app_version + '/users/logout', 'controller': LogoutService()},
        {'url': '/access-denied'.format(app_version), 'controller': AccessDeniedPage()}
    ]
