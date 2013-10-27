bitsnoop - Unofficial Python API for [BitSnoop](http://www.bitsnoop.com/)
==========================================================================


.. image:: https://travis-ci.org/infothrill/python-bitsnoop.png
    :target: https://travis-ci.org/infothrill/python-bitsnoop

.. image:: https://coveralls.io/repos/infothrill/python-bitsnoop/badge.png
        :target: https://coveralls.io/r/infothrill/python-bitsnoop

.. image:: https://badge.fury.io/py/bitsnoop.png
    :target: http://badge.fury.io/py/bitsnoop

.. image:: https://pypip.in/d/bitsnoop/badge.png
        :target: https://crate.io/packages/bitsnoop/


Installation
=============

.. code-block:: bash

	$ python setup.py install

.. code-block:: bash

    NOT AVAILABLE yet!
    $ pip install bitsnoop


Requirements
============
Currently python 2.7, 3.2 and 3.3


Usage
=====
.. code-block:: python

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
