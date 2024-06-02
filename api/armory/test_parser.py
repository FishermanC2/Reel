import unittest
from parsers import Bait
import base64

class TestBaitParser(unittest.TestCase):
    def test_default_bait_parse(self):
        encoded_bait = base64.b64decode(Bait.b64_encode("fetch.js").encode()).decode()
        self.assertNotEqual(encoded_bait.find('127.0.0.1:5000'), -1)
        self.assertNotEqual(encoded_bait.find('http'), -1)

    def test_bait_parser_with_conf(self):
        conf = {
            '--server': '177.0.0.1:5000',
            '--protocol': 'https',
            '--format' : 'b64'
        }
        encoded_bait = base64.b64decode(Bait.b64_encode("fetch.js", **conf).encode()).decode()
        self.assertNotEqual(encoded_bait.find('177.0.0.1:5000'), -1)
        self.assertNotEqual(encoded_bait.find('https'), 1)


if __name__ == '__main__':
    unittest.main()
