import sys
import logging
import json
from datetime import datetime, timedelta

import requests

from bitsnoop.constant_type import Constants


if sys.version_info >= (3, 0):
    unicode = str
else:
    pass

FAKESKAN_URL = "http://bitsnoop.com/api/fakeskan.php"


class FAKESKAN(Constants):
    class CODE:
        ERROR = 0
        NOTFOUND = 1
        VERIFIED = 2
        GOOD = 3
        NONE = 4
        BAD = 5
        FAKE = 6

    class DESCRIPTION:
        ERROR = "hash not specified or internal error has occured. If you did specify hash, retry request in 10-15 minutes"
        NOTFOUND = "torrent does not exist in index"
        VERIFIED = "torrent is verified"
        GOOD = "torrent has some 'good' votes, not verified yet"
        NONE = "no votes or too little of them to decide"
        BAD = "some 'bad' votes, not fake yet"
        FAKE = "torrent is fake"


class CachedFakeskan(object):
    '''
    A little wrapper that allows caching of the fakeskan values.
    '''
    def __init__(self, cache=None, expiry=86400, url=FAKESKAN_URL):
        '''
        Constructor
        :param cache: anything that implements a dict style interface
        :param expiry: number of seconds until cache entries are expired
        :param url: the URL of the fakeskan service
        '''
        if cache is None:
            cache = {}
        self._cache = cache
        self._expiry = timedelta(seconds=expiry)
        self._url = url

    def cache(self):
        return dict(self._cache)

    def call(self, key):
        if key in self._cache:
            dummycode, dt = self._cache[key]
            if datetime.now() - dt > self._expiry:
                logging.debug("expire fakeskan cache for '%s'!", key)
                self._cache[key] = (fakeskan(key), datetime.now())
            else:
                pass
                # logging.info("cache hit!")
        else:
            logging.info("no fakeskan cache for '%s': querying!", key)
            self._cache[key] = (fakeskan(key), datetime.now())
        entry = self._cache[key]
        if entry[0] == FAKESKAN.CODE.ERROR:
            # don't cache errors
            del self._cache[key]
            return entry
        return self._cache[key][0]

    def __call__(self, key):
        return self.call(key)


def fakeskan(btih, url=FAKESKAN_URL):
    assert type(btih) in (str, unicode)
    assert len(btih) == 40, "Length of Bittorrent info hash should be 40 but isn't: '%s'" % btih
    __FAKESKAN_MAP = {
        "ERROR": FAKESKAN.CODE.ERROR,
        "NOTFOUND": FAKESKAN.CODE.NOTFOUND,
        "VERIFIED": FAKESKAN.CODE.VERIFIED,
        "GOOD": FAKESKAN.CODE.GOOD,
        "NONE": FAKESKAN.CODE.NONE,
        "BAD": FAKESKAN.CODE.BAD,
        "FAKE": FAKESKAN.CODE.FAKE,
    }
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    r = requests.get(url, params={"hash": btih, "json": "1"}, headers=headers, timeout=120)
    assert r.headers['content-type'].find('application/json') >= 0, "Wrong content-type received: %s" % r.headers['content-type']
    return __FAKESKAN_MAP[json.loads(r.text)]


def main():
    print fakeskan("DAAC7008E2E3A6E4321950C131690ACA20C5A08A")


if __name__ == '__main__':
    sys.exit(main())
