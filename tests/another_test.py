import unittest


class AnotherTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_numbers(self):
        self.assertEqual(2, 2)


if __name__ == '__main__':
    unittest.main()
