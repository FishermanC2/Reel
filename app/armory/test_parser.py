import unittest
from parsers import BaitParser, Bait

# TODO: update parser expected results
URL_ENCODED_FETCH_BAIT = (b"LyoNCkRlZmF1bHQgcGF5bG9hZCBmb3IgaG9va2luZyBicm93c2VycyB0byB0aGUgZmlzaGVybWFuJ3MgYm9hdCB1c2luZyBmZXRjaCBhcGkNCiovDQoNCihmdW5jdGlvbigpIHsNCiAgICBhc3luYyBmdW5jdGlvbiBzZW5kUmVxdWVzdCgpIHsNCiAgICAgICAgY29uc3QgcmVzID0gYXdhaXQgZmV0Y2goDQogICAgICAgICAgICAnaHR0cDovLzEyNy4wLjAuMTo1MDAwL2FsaXZlJywNCiAgICAgICAgICAgIHsNCiAgICAgICAgICAgICAgICAnbW9kZScgOiAnbm8tY29ycycsDQogICAgICAgICAgICAgICAgJ21ldGhvZCcgOiAiUE9TVCINCiAgICAgICAgICAgIH0NCiAgICAgICAgKQ0KICAgIH0NCg0KICAgIHNlbmRSZXF1ZXN0KCk7DQogICAgc2V0SW50ZXJ2YWwoc2VuZFJlcXVlc3QsIDMwMDAwKQ0KfSk=")

class TestBaitParser(unittest.TestCase):
    def test_bait_parser(self):
        bait_parser = BaitParser(Bait.FETCH)
        encoded_bait = bait_parser.b64_encode()

        self.assertEqual(URL_ENCODED_FETCH_BAIT, encoded_bait)


if __name__ == '__main__':
    unittest.main()
