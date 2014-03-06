bitsnoop - Unofficial Python API for `BitSnoop <http://www.bitsnoop.com/>`_
===========================================================================

.. image:: https://travis-ci.org/infothrill/python-bitsnoop.png
    :target: https://travis-ci.org/infothrill/python-bitsnoop

.. image:: https://coveralls.io/repos/infothrill/python-bitsnoop/badge.png
        :target: https://coveralls.io/r/infothrill/python-bitsnoop

.. image:: https://requires.io/github/infothrill/python-bitsnoop/requirements.png?branch=master
   :target: https://requires.io/github/infothrill/python-bitsnoop/requirements/?branch=master
   :alt: Requirements Status

Currently implemented:

A001 — FakeSkan status of torrent
    module bitsnoop.fakeskan


Usage
=====
.. code-block:: python

	from bitsnoop import fakeskan

	fk = fakeskan.Fakeskan()  # create a fakeskan object with default URL

	if fk("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A") == fakeskan.VERIFIED:
		print("This torrent is verified!")


Since bitsnoop.com implements some form of rate limiting on queries,
we provide a minimal caching interface:

.. code-block:: python

	dictcache = {}

	fk = fakeskan.Fakeskan(cache=dictcache, cache_expiry=120)

	if fk("43DBF6EBC059CD97ACAE7CAF308A0E050A7EC51A") == fakeskan.VERIFIED:
		print("This torrent is verified!")


The cache object is treated like a dictionary and can thus also be an object
that implements persistency (like shelve).


Installation
============

.. code-block:: bash

    $ python setup.py install

.. code-block:: bash

    NOT AVAILABLE yet!
    $ pip install bitsnoop


Requirements
============
Currently python 2.7, 3.1, 3.2 and 3.3


Contribute
==========

If you want to add any new features, or improve existing ones, feel free to send a pull request!
