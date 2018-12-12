import unittest


class MainTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_numbers_3_4(self):
        self.assertEqual(2, 2)


if __name__ == '__main__':
    unittest.main()
