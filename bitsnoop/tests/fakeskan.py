import unittest
import sys
import logging
import datetime

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

from bitsnoop import Fakeskan, FakeskanCached, FAKESKAN
from .server import BitsnoopFakeSkanApp


class FakeskanTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start local server
        """
        cls.server = BitsnoopFakeSkanApp('localhost', 8000)
        cls.url = "http://localhost:8000/api/fakeskan.php"
        cls.server.start()

    def test_fakeskan(self):
        fakeskan = Fakeskan(self.url)
        test_data = {
                       "03DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.ERROR,
                       "13DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.NOTFOUND,
                       "23DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.VERIFIED,
                       "33DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.GOOD,
                       "43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.NONE,
                       "53DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.BAD,
                       "63DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": FAKESKAN.CODE.FAKE,
                       }
        for key in test_data:
            self.assertEqual(test_data[key], fakeskan(key))

    @classmethod
    def tearDownClass(cls):
        """
        Stop local server.
        """
        cls.server.stop()


class FakeskanCachedTestClass(unittest.TestCase):
    def test_fakeskan_cache(self):
        # this will effectively test if we get a valid result without
        # ever making any http connections
        cache = {
                 "43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A":
                    (FAKESKAN.CODE.GOOD, datetime.datetime.now())
                 }
        fakeskan = FakeskanCached(cache, url="http://nonexistant.example.com/")
        result = fakeskan("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A")
        self.assertEqual(FAKESKAN.CODE.GOOD, result)
