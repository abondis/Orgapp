#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import sys
sys.path.extend(['../lib'])
from tasks import Orgapp
import unittest


class TestTasks(unittest.TestCase):

    def setUp(self):
        self.t = Orgapp()

    def tearDown(self):
        pass

    def test_add(self):
        self.t.add("TESTUNIT1", 0, "new")
        self.t.add("TESTUNIT2", 1)
        self.t.add("TESTUNIT3", status="new")
        self.t.add("TESTUNIT4")
        l = self.t.ls()
        self.assertEqual(l['new'][0].name, "TESTUNIT1")
        self.assertEqual(l['new'][0].position, 0)
        self.assertEqual(l['new'][0].status_id, 1)


if __name__ == '__main__':
    unittest.main()
