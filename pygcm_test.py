# -*- coding:utf-8 -*-
"""

Pygcm unittests

"""

import unittest
from pygcm.manage import GCMManager
from pygcm.base_config import MAX_NUMBER_OF_TARGET


class ManagerTest(unittest.TestCase):
    def setUp(self):
        self.m = GCMManager('AIzaSyD1aoD55ZBAukBDhOg957bD2dxxMGt8u8Q')
        self.id = """
                
                """
        self.message = 'pygcm test'
    
    def test_single_send(self):
        success = self.m.send(self.id, self.message)
        self.assertTrue(success)

    def test_multi_send(self):
        ids = [self.id] * MAX_NUMBER_OF_TARGET
        success = self.m.send(ids, self.message)
        self.assertTrue(success)

    def test_multi_send_split(self):
        ids = [self.id] * MAX_NUMBER_OF_TARGET * 3
        success = self.m.send(ids, self.message)
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
