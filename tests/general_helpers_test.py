import unittest
from helpers.general_helpers import GeneralHelpers


class GeneralHelpersTest(unittest.TestCase):
    """
    Helpers test cases
    :author: zoltan.csontos.dev@gmail.com
    """

    def setUp(self):
        """
        Setup the general helpers before test run
        :return:
        """
        self.helpers = GeneralHelpers()
        pass

    def test_directory_contents(self):
        """
        Tests the directory contents grab mechanism
        :return:
        """
        expected_file_name = 'test_file.txt'

        dir_contents = self.helpers.get_dir_contents('tests/test_dir')
        actual_files = [item['file'] for item in dir_contents]

        self.assertEqual(len(actual_files), 1)
        self.assertEqual(actual_files[0], expected_file_name)

    def test_directory_structure(self):
        """
        Tests the directory structure mechanism
        :return:
        """
        expected_keyword = 'tests/test_dir'
        dir_structure = self.helpers.get_dir_structure('tests/test_dir')
        print(dir_structure)
        self.assertEqual(len(dir_structure), 1)

        first_item = dir_structure[0]
        self.assertTrue(expected_keyword in first_item['path'])
        self.assertTrue(first_item['url'] == '')
