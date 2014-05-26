# -*- coding: utf-8 -*-

import logging
import json
from datetime import datetime, timedelta

import requests

logger = logging.getLogger(__name__)

FAKESKAN_URL = "http://bitsnoop.com/api/fakeskan.php"


ERROR = 0
NOTFOUND = 1
VERIFIED = 2
GOOD = 3
NONE = 4
BAD = 5
FAKE = 6

ERROR_DESCRIPTION = "hash not specified or internal error has occured. If you did specify hash, retry request in 10-15 minutes"
NOTFOUND_DESCRIPTION = "torrent does not exist in index"
VERIFIED_DESCRIPTION = "torrent is verified"
GOOD_DESCRIPTION = "torrent has some 'good' votes, not verified yet"
NONE_DESCRIPTION = "no votes or too little of them to decide"
BAD_DESCRIPTION = "some 'bad' votes, not fake yet"
FAKE_DESCRIPTION = "torrent is fake"


class Fakeskan(object):
    '''
    A class to instantiate a fakeskan api client pointing to the optional
    api URL.
    '''
    def __init__(self, url=FAKESKAN_URL, cache=None, cache_expiry=86400):
        '''
        :param url: the URL of the fakeskan service
        :param cache: anything that implements a dict style interface
        :param cache_expiry: number of seconds until cache entries are expired
        '''
        self._cache = cache
        self._cache_expiry = timedelta(seconds=cache_expiry)
        self._url = url

    def _cached_call(self, key):
        now = datetime.now()
        try:
            code, cachedt = self._cache[key]
        except KeyError:
            code = None
        else:
            if now - cachedt > self._cache_expiry:
                logger.debug("expiring fakeskan cache for '%s'!", key)
                code = None
        finally:
            if code is None:
                code = fakeskan(key, self._url)
            if code is not ERROR:
                self._cache[key] = (code, now)
        return code

    def __call__(self, key):
        if self._cache is None:
            return fakeskan(key, self._url)
        else:
            return self._cached_call(key)


def fakeskan(btih, url=FAKESKAN_URL):
    '''
    Get the FAKESKAN.CODE for the given bittorrent info hash

    :param btih: the string representation of a bittorent info hash
    :param url: optional URL for the bitsnoop fakeskan API
    '''
    if not isinstance(btih, str):
        raise ValueError("the provided info hash must be a string, not %s!" % str(type(btih)))
    if len(btih) != 40:
        raise ValueError("Length of info hash must be 40 but isn't: '%r'" % btih)
    _fakeskan_map = {
        "ERROR": ERROR,
        "NOTFOUND": NOTFOUND,
        "VERIFIED": VERIFIED,
        "GOOD": GOOD,
        "NONE": NONE,
        "BAD": BAD,
        "FAKE": FAKE,
    }
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    r = requests.get(url, params={"hash": btih, "json": "1"}, headers=headers, timeout=120)
    assert r.headers['content-type'].find('application/json') >= 0, "Wrong content-type received: '%s'" % r.headers['content-type']
    return _fakeskan_map[json.loads(r.text)]
