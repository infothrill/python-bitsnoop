Unofficial Python API for [BitSnoop](http://www.bitsnoop.com/).

[![Build Status](https://travis-ci.org/infothrill/python-bitsnoop.png)](https://travis-ci.org/infothrill/python-bitsnoop)    [![Coverage Status](https://coveralls.io/repos/infothrill/python-bitsnoop/badge.png)](https://coveralls.io/r/infothrill/python-bitsnoop)

Installation
=============

	$ python setup.py install

    NOT AVAILABLE yet
    ## $ pip install bitsnoop


Python versions
===============
Currently python 2.7, 3.2 and 3.3


Usage
=====
	from bitsnoop import Fakeskan, FAKESCAN

	fakeskan = Fakeskan()  # create a fakeskan object with default URL

	if fakeskan("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A") == FAKESCAN.CODE.VERIFIED:
		print("This torrent is verified!")

	# since bitsnoop.com implements some form of rate limiting on queries,
	# we provide a minimal caching interface:

	from bitsnoop import FakeskanCached
	cache = {}
	fakeskan = FakeskanCached(cache=cache)
	if fakeskan("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A") == FAKESCAN.CODE.VERIFIED:
		print("This torrent is verified!")

	# Alternatively, the cache can be a shelve object for example:
	import shelve
	cache = shelve.open("fakeskan")
	fakeskan = FakeskanCached(cache=cache)
	if fakeskan("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A") == FAKESCAN.CODE.VERIFIED:
		print("This torrent is verified!")
	# beware of thread-seafety with the cache object. shelve is a toy!


Contribute
==========

If you want to add any new features, or improve existing ones, feel free to send a pull request!
