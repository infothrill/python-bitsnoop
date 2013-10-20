import unittest
import sys
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

from bitsnoop import fakeskan
from server import BitsnoopFakeSkanApp


class FakeskanTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start local server
        """
        cls.server = BitsnoopFakeSkanApp('localhost', 8000)
        cls.server.start()

    def test_fakeskan(self):
        url = "http://localhost:8000/api/fakeskan.php"
        fakeskan("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A", url)

    @classmethod
    def tearDownClass(cls):
        """
        Stop local server.
        """
        cls.server.stop()
