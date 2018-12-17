import unittest
from helpers.general_helpers import GeneralHelpers
from core.sys_modules.authentication.PermissionGroups_model import PermissionGroupsModel
from core.sys_modules.authentication.Users_model import UsersModel
from core.sys_modules.authentication.UsersPermissions_model import UsersPermissionsModel
from core.sys_modules.authentication.UserToken_model import UserTokenModel
from core.sys_modules.authentication.routes import routes as user_routes
from core.sys_modules.swagger.routes import routes as swagger_routes


class GeneralHelpersTest(unittest.TestCase):
    """
    Helpers test cases
    :author: zoltan.csontos.dev@gmail.com
    """

    SYSTEM_MODEL_LIST = [
        PermissionGroupsModel.__name__,
        UsersModel.__name__,
        UsersPermissionsModel.__name__,
        UserTokenModel.__name__
    ]

    SYSTEM_MODULES_URL_LIST = []

    def setUp(self):
        """
        Setup the general helpers before test run
        :return:
        """
        self.helpers = GeneralHelpers()
        self.SYSTEM_MODULES_URL_LIST = self.SYSTEM_MODULES_URL_LIST + \
                                       [item['url'] for item in user_routes] + \
                                       [item['url'] for item in swagger_routes]
        pass

    def test_directory_contents(self):
        """
        Tests the directory contents grab mechanism
        :return:
        """
        expected_file_name = 'test_file.txt'

        dir_contents = self.helpers.get_dir_contents('../tests/test_dir')
        actual_files = [item['file'] for item in dir_contents]

        self.assertEqual(len(actual_files), 1)
        self.assertEqual(actual_files[0], expected_file_name)

    def test_directory_structure(self):
        """
        Tests the directory structure mechanism
        :return:
        """
        expected_keyword = 'tests/test_dir'
        dir_structure = self.helpers.get_dir_structure('../tests/test_dir')
        self.assertEqual(len(dir_structure), 1)

        first_item = dir_structure[0]
        self.assertTrue(expected_keyword in first_item['path'])
        self.assertTrue(first_item['url'] == '')

    def test_model_grabbing_functionality(self):
        """
        Test the model grabbing functionality on system modules
        :return:
        """
        models = [model.__name__ for model in self.helpers.get_models()]
        for sys_model in self.SYSTEM_MODEL_LIST:
            self.assertTrue(sys_model in models)

    def test_app_route_grabbing_functionality(self):
        """
        Tests the app url grabbing functionality
        :return:
        """
        app_urls = [item['url'] for item in self.helpers.get_app_routes()]
        for item in self.SYSTEM_MODULES_URL_LIST:
            self.assertTrue(item in app_urls)
