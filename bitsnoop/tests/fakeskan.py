# -*- coding: utf-8 -*-

import unittest
import os
import sys
import logging
import datetime

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

from bitsnoop import fakeskan
from .server import BitsnoopFakeSkanApp


class FakeskanServerTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start local server in clean environment
        """
        # remove proxy environment variables for this test
        for env_var in ('HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy'):
            if env_var in os.environ:
                del os.environ[env_var]
        cls.server = BitsnoopFakeSkanApp('localhost', 8000)
        cls.url = "http://localhost:8000/api/fakeskan.php"
        cls.server.start()

    def test_fakeskan_input_validation(self):
        fk = fakeskan.Fakeskan(self.url)
        self.assertRaises(ValueError, fk, "sdsdg")
        self.assertRaises(ValueError, fk, None)

    def test_fakeskan_connections(self):
        fk = fakeskan.Fakeskan(self.url)
        test_data = {
                       "03DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.ERROR,
                       "13DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.NOTFOUND,
                       "23DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.VERIFIED,
                       "33DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.GOOD,
                       "43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.NONE,
                       "53DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.BAD,
                       "63DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A": fakeskan.FAKE,
                       }
        for key in test_data:
            self.assertEqual(test_data[key], fk(key))

    def test_fakeskan_cachefill(self):
        # test if we actually fill the cache
        cache_expiry = 10
        cache = {}
        fk = fakeskan.Fakeskan(url=self.url, cache=cache, cache_expiry=cache_expiry)
        result = fk("33DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A")
        self.assertEqual(fakeskan.GOOD, result)
        self.assertEqual(1, len(cache))

    def test_fakeskan_cachehit(self):
        # test if we hit a cache result
        cache_expiry = 10
        cache = {
                 "99DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A":
                    (fakeskan.BAD, datetime.datetime.now() - datetime.timedelta(seconds=3))
                 }
        fk = fakeskan.Fakeskan(url=self.url, cache=cache, cache_expiry=cache_expiry)
        result = fk("99DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A")
        self.assertEqual(fakeskan.BAD, result)
        self.assertEqual(1, len(cache))

    def test_fakeskan_cache_expiry(self):
        # test if we get cache expiration
        cache_expiry = 1
        cache = {
                 "33DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A":
                    (fakeskan.ERROR, datetime.datetime.now() - datetime.timedelta(seconds=3))
                 }
        fk = fakeskan.Fakeskan(url=self.url, cache=cache, cache_expiry=cache_expiry)
        result = fk("33DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A")
        self.assertEqual(fakeskan.GOOD, result)
        self.assertEqual(1, len(cache))

    def test_fakeskan_dontcache_errors(self):
        # make sure errors are not cached
        cache = {}
        fk = fakeskan.Fakeskan(url=self.url, cache=cache)
        result = fk("03DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A")
        self.assertEqual(fakeskan.ERROR, result)
        self.assertEqual(0, len(cache))

    @classmethod
    def tearDownClass(cls):
        """
        Stop local server.
        """
        cls.server.stop()


class FakeskanNoServerTestClass(unittest.TestCase):
    def test_fakeskan_cache(self):
        # this will effectively test if we get a valid result without
        # ever making any http connections
        cache = {
                 "43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A":
                    (fakeskan.GOOD, datetime.datetime.now())
                 }
        fk = fakeskan.Fakeskan(cache=cache, url="http://nonexistant.example.com/")
        result = fk("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A")
        self.assertEqual(fakeskan.GOOD, result)
