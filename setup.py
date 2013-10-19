#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pybitsnoop',
    version='0.1',
    install_requires=['requests'],
    author='Paul Kremer',
    author_email='',
    packages=['bitsnoop'],
    test_suite='bitsnoop/tests',
    url='https://github.com/infothrill/python-bitsnoop',
    license='MIT License',
    description='Unofficial Python API for parts of bitsnoop.com',
    long_description='Unofficial Python API for BitSnoop. Usage: https://github.com/infothrill/python-bitsnoop.',
)
