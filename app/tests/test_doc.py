#!/usr/bin/env python
#-=- encoding: utf-8 -=-

import sys
sys.path.extend(['../lib'])
import os
from doc import Doc
import unittest
import ConfigParser
import shutil


class TestDoc(unittest.TestCase):
    def setUp(self):
        """setUp:
            * creates folders for the doc testing
            * creates a testing repository
            * writes a test file"""
        c = ConfigParser.RawConfigParser()
        c.add_section('doc')
        c.set('doc', 'doc', '/tmp/test/doc')
        c.set('doc', 'cache', '/tmp/test/cache')
        c.set('doc', 'repo', '/tmp/test')
        self.d = Doc(c)
        with open(self.d.doc + '/test', 'w') as f:
            f.write("UNITTEST")
        self.assertTrue(os.path.exists(self.d.repo))
        self.assertTrue(os.path.exists(self.d.cache_path))
        self.assertTrue(os.path.exists(self.d.doc))

    def tearDown(self):
        os.remove(self.d.doc + '/test')
        shutil.rmtree(self.d.doc)
        shutil.rmtree(self.d.cache_path)
        shutil.rmtree(self.d.repo)

    def test_render(self):
        """test doc rendering"""
        render = self.d.render("/test", 'copy')
        self.assertTrue(render == "UNITTEST")

    def test_cache(self):
        """test doc caching"""
        self.d.cache('/test')
        with open(self.d.cache_path + '/test', 'r') as f:
            render = f.read()
        self.assertTrue(render == "UNITTEST")

    def test_save(self):
        self.d.save('/test', "TESTSAVE")
        with open(self.d.doc + '/test', 'r') as f:
            render = f.read()
        self.assertTrue(render == "TESTSAVE")

    def test_list_pages(self):
        self.d.save('/page.md', "TESTLIST")
        l = self.d.list_pages()
        self.assertTrue(l[0] == "page")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDoc)
    unittest.TextTestRunner(verbosity=2).run(suite)
