#!/usr/bin/env python
#-=- encoding: utf-8 -=-
import sys
sys.path.extend(['../lib'])
from tasks import Orgapp
import unittest


class TestTasks(unittest.TestCase):

    def setUp(self):
        self.t = Orgapp()
        self.t.add("TESTUNIT1", 0, "new")
        self.t.add("TESTUNIT2", 1)
        self.t.add("TESTUNIT3", status="running")
        self.t.add("TESTUNIT4")

    def tearDown(self):
        self.t.rm(1)
        self.t.rm(2)
        self.t.rm(3)
        self.t.rm(4)

    def test_ls(self):
        l = self.t.ls()
        self.assertEqual(l['new'][0].name, "TESTUNIT1")
        self.assertEqual(l['new'][0].position, 0)
        self.assertEqual(l['new'][0].status_id, 1)
        self.assertEqual(l['new'][1].name, "TESTUNIT2")
        self.assertEqual(l['new'][1].position, 1)
        self.assertEqual(l['new'][1].status_id, 1)
        self.assertEqual(l['running'][0].name, "TESTUNIT3")
        self.assertEqual(l['running'][0].position, 2)
        self.assertEqual(l['running'][0].status_id, 2)
        self.assertEqual(l['new'][2].name, "TESTUNIT4")
        self.assertEqual(l['new'][2].position, 3)
        self.assertEqual(l['new'][2].status_id, 1)

    def test_move(self):
        l = self.t.ls()
        self.t.status(1, 'running')
        self.t.move(1, 3, 'running')
        self.assertEqual(l['running'][1].name, "TESTUNIT1")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTasks)
    unittest.TextTestRunner(verbosity=2).run(suite)
