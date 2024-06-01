import unittest
from parsers import Bait
import base64

class TestBaitParser(unittest.TestCase):
    def test_default_bait_parse(self):
        encoded_bait = base64.b64decode(Bait.b64_encode("fetch.js").encode()).decode()
        self.assertNotEqual(encoded_bait.find('127.0.0.1:5000'), -1)

    def test_bait_parser_with_conf(self):
        encoded_bait = base64.b64decode(Bait.b64_encode("fetch.js", "177.0.0.1:5000").encode()).decode()
        self.assertNotEqual(encoded_bait.find('177.0.0.1:5000'), -1)


if __name__ == '__main__':
    unittest.main()
