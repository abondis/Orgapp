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
        c.add_section('repo')
        c.set('doc', 'doc', '/doc/')
        c.set('doc', 'cache', '/tmp/test/cache/')
        c.set('repo', 'repo_root', '/tmp/test/')
        c.set('repo', 'git_repos', 'repogit')
        self.d = Doc(c)
        self.assertTrue(os.path.exists(self.d.repo_root))
        self.assertTrue(os.path.exists(self.d.cache_path))
        self.assertTrue(os.path.exists(self.d.repo_root +
            'repogit' +
            self.d.doc))
        with open(self.d.repo_root +
                'repogit' +
                self.d.doc +
                '/test', 'w') as f:
            f.write("UNITTEST")

    def tearDown(self):
        os.remove(self.d.repo_root + 'repogit' + self.d.doc + '/test')
        _path = self.d.repo_root + 'repogit'
        shutil.rmtree(_path + self.d.doc)
        shutil.rmtree(self.d.cache_path)
        shutil.rmtree(self.d.repo_root)

    def test_render(self):
        """test doc rendering"""
        render = self.d.render("/test", 'repogit', 'copy')
        self.assertTrue(render == "UNITTEST")

    def test_cache(self):
        """test doc caching"""
        self.d.cache('/test', 'repogit')
        with open(self.d.cache_path + 'repogit' + '/test', 'r') as f:
            render = f.read()
        self.assertTrue(render == "UNITTEST")

    def test_save(self):
        self.d.save('/test', "TESTSAVE", 'repogit')
        with open(self.d.repo_root +
                'repogit' +
                self.d.doc +
                '/test', 'r') as f:
            render = f.read()
        self.assertTrue(render == "TESTSAVE")

    def test_list_pages(self):
        self.d.save('/page.md', "TESTLIST", 'repogit')
        l = self.d.list_pages('repogit')
        self.assertTrue(l[0] == "page")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDoc)
    unittest.TextTestRunner(verbosity=2).run(suite)
