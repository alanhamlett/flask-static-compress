# -*- coding: utf-8 -*-


try:
    # Python 2.6
    import unittest2 as unittest
except ImportError:
    # Python >= 2.7
    import unittest


class BaseTestCase(unittest.TestCase):

    def test_can_wrap_jac(self):
        from flask_static_compress import FlaskStaticCompress
        self.assertIsNotNone(FlaskStaticCompress)
