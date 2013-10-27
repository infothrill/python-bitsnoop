# -*- coding: utf-8 -*-

import unittest

from bitsnoop.constant_type import ConstantType, Constants


class ConstantTypeTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_Constants(self):
        self.assertEqual(type(ConstantType), type)
        self.assertEqual(type(Constants), ConstantType)

        class FOO(Constants):
            BAR = 1

        self.assertTrue(repr(Constants).startswith("ConstantType"))
        self.assertTrue(repr(FOO).startswith("ConstantType"))
        self.assertEqual(ConstantType, type(FOO))
        self.assertEqual(1, FOO.BAR)
        self.assertEqual(str, type(str(FOO)))
        self.assertEqual("1", str(FOO.BAR))
