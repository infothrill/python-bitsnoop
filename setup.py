#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


classifiers = [line.strip() for line in """
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: DFSG approved
License :: OSI Approved
License :: OSI Approved :: MIT License
Topic :: Software Development :: Libraries :: Python Modules
Environment :: Console
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
Operating System :: POSIX :: BSD :: FreeBSD
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
""".splitlines() if len(line) > 0]

setup(
    name='bitsnoop',
    packages=['bitsnoop', 'bitsnoop.tests'],
    version='0.1',
    author='Paul Kremer',
    author_email="@".join(("paul", "spurious.biz")),  # avoid spam,
    url='https://github.com/infothrill/python-bitsnoop',
    license='MIT License',
    description='Unofficial Python API for parts of bitsnoop.com',
    long_description='Unofficial Python API for BitSnoop. Usage: https://github.com/infothrill/python-bitsnoop.',
    install_requires=['requests'],
    classifiers=classifiers,
    test_suite='bitsnoop.tests',
    tests_require=['bottle==0.11.6'],
)
