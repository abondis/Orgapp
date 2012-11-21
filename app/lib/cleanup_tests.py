#!/usr/bin/env python
#-=- encoding: utf-8 -=-

import unittest
#import cleanup
from cleanup import *
from hashlib import md5
import os
import shutil

test_doc_path = '/tmp/mydoc'
test_git_path = '/tmp/git_test'
test_hg_path = '/tmp/hg_test'
test_proj_path = '/tmp/myproject'
_now = str(datetime.datetime.now())

class TasksTests(unittest.TestCase):

    def testAdd(self):
        """ Add a 'test' task"""
        _now = str(datetime.datetime.now())
        Tasks.create(
                name='test',
                md5hash=md5('test'+_now).hexdigest(),
                position=30)
        _t = Tasks.get(name='test')
        self.failUnless(_t.name == 'test')
        self.failUnless(_t.md5hash == md5('test'+_now).hexdigest())
        self.failUnless(_t.project.name == DEFAULTPROJECT)
        self.failUnless(_t.status.name == DEFAULTSTATUS)


    def testRename(self):
        """ Rename 'test' to 'Test'"""
        _t = Tasks.get_or_create(
                name='test',
                md5hash=md5('test'+_now).hexdigest(),
                position=30)
        _md5 = _t.md5hash
        _t.rename('Test')
        self.failUnless(_t.name == 'Test')
        self.failUnless(_t.md5hash == _md5)
        self.failUnless(_t.project.name == DEFAULTPROJECT)
        self.failUnless(_t.status.name == DEFAULTSTATUS)

    def testChangePos(self):
        """ Move 'Test' to pos 1"""
        _t = Tasks.get_or_create(
                name='test',
                md5hash=md5('test'+_now).hexdigest(),
                position=30)
        _t.position = 20
        _t.save()
        self.failUnless( _t.position == 20)

    def testDelete(self):
        """ Delete 'Test' from the list"""
        _t = Tasks.get_or_create(
                name='test',
                md5hash=md5('test'+_now).hexdigest(),
                position=30)
        _count = _t.delete_instance()
        self.failUnless(_count == 1)

class RepoTest(unittest.TestCase):
    # FIXME: remove directories at the end
    """ Test repo can be hg or git """
    def testOpenRepo(self):
        """ Test opening a repo"""
        Repo(test_hg_path+'', 'hg')
        self.failUnless( os.path.exists(test_hg_path+''))
        self.failUnless( os.path.exists(test_hg_path+'/.hg'))
        Repo(test_git_path+'', 'git')
        self.failUnless( os.path.exists(test_git_path+''))
        self.failUnless( os.path.exists(test_git_path+'/.git'))

    def testAddFile(self):
        """ Test adding a file to the repo"""
        _r = Repo(test_hg_path+'', 'hg')
        with open(test_hg_path+'/TestFile', 'w') as f:
            f.write("UNITTEST")
        _r.add_file(test_hg_path+'/TestFile')
        self.failUnless( os.path.exists(test_hg_path+'/TestFile'))
        _r = Repo(test_git_path+'', 'git')
        with open(test_git_path+'/TestFile', 'w') as f:
            f.write("UNITTEST")
        _r.add_file(test_git_path+'/TestFile')
        self.failUnless( os.path.exists(test_git_path+'/TestFile'))

    def testrmFile(self):
        """ Test removing a file from the repo"""
        pass
    @classmethod
    def tearDownClass(self):
        shutil.rmtree(test_hg_path)
        shutil.rmtree(test_git_path)
    
class ProjectTest(unittest.TestCase):
    """ Test project with a wiki and task db and task files"""

    def testInit(self):
        _p = Project('projectname', test_proj_path+'', 'hg')
        self.failUnless(_p.name == 'projectname')
        self.failUnless(_p.path == test_proj_path+'')
        self.failUnless(_p.vcs_type == 'hg')
        self.failUnless(os.path.exists(test_proj_path+''))
        self.failUnless(os.path.exists(test_proj_path+'/projectname/.hg'))
        self.failUnless(os.path.exists(test_proj_path+'/projectname/doc'))
        self.failUnless(os.path.exists(test_proj_path+'/projectname/tasks'))

    def testCreateTask(self):
        _p = Project('projectname', test_proj_path+'', 'hg')
        _p.create_task('unittest')
        _t1 = Tasks.get(name='unittest')
        # FIXME: check that file is created too
        self.failUnless(_t1.name == 'unittest' )
        self.failUnless(_t1.project.name == 'unknown' )
        self.failUnless(
            os.path.exists( test_proj_path+'/projectname/tasks/unittest.md'))

    def testCreateDoc(self):
        _p = Project('projectname', test_proj_path+'', 'hg')
        _p.create_doc('blah', 'this is MY content')
        with open(test_proj_path+'/projectname/doc/blah.md') as _f:
            _c = _f.read()
        self.failUnless( _c == 'this is MY content')

    def testRenameProject(self):
        pass

    def testRenameTask(self):
        pass

    def testListTasks(self):
        pass

    def testAddDocuments(self):
        pass

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(test_proj_path)
        # default project cache is in /tmp
        shutil.rmtree('/tmp/projectname')

class DocTest(unittest.TestCase):
    def testCreateDoc(self):
        _doc = Doc(test_doc_path+'', test_doc_path+'scache')
        _doc.create_doc('mydoc.something', 'this is my content')
        self.failUnless(os.path.exists(test_doc_path+'/mydoc.something'))
        self.failUnless(os.path.exists(test_doc_path+'scache'))
        with open(test_doc_path+'/mydoc.something') as _f:
            _c = _f.read()
        self.failUnless( _c == 'this is my content')

    def testCacheDoc(self):
        _doc = Doc(test_doc_path+'', test_doc_path+'scache')
        _doc.create_doc('mydoc.md', 'this is my content')
        _doc.cache('mydoc.md')
        with open(test_doc_path+'scache/mydoc.md') as _f:
            _c = _f.read()
        self.failUnless(os.path.exists(test_doc_path+'scache/mydoc.md'))
        self.failUnless( _c == '<p>this is my content</p>')

    def testRenderDoc(self):
        _doc = Doc(test_doc_path+'', test_doc_path+'scache')
        _doc.create_doc('mydoc.truc', 'this is my content')
        _r = _doc.render('mydoc.truc')
        self.failUnless( _r == 'this is my content')
        _doc.create_doc('mydoc.md', 'this is my content')
        _r = _doc.render('mydoc.md')
        self.failUnless( _r == '<p>this is my content</p>')

    def testGetDoc(self):
        _doc = Doc(test_doc_path+'', test_doc_path+'scache')
        _doc.create_doc('mydoc.truc', 'this is my content')
        _doc.cache('mydoc.truc')
        _c = _doc.get_doc('mydoc.truc')
        self.failUnless( _c == 'this is my content')
        _doc.create_doc('mydoc.md', 'this is my content')
        _doc.cache('mydoc.md')
        _c = _doc.get_doc('mydoc.md')
        self.failUnless( _c == '<p>this is my content</p>')

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(test_doc_path+'', ignore_errors=True)
        shutil.rmtree(test_doc_path+'scache', ignore_errors=True)
        shutil.rmtree(test_hg_path+'', ignore_errors=True)
        shutil.rmtree(test_git_path+'', ignore_errors=True)

class TasklistTest(unittest.TestCase):
    def testAddTask(self):
        """Add a task in the task list"""
        # to add a task and check status relatively to project
        _tl = Tasklist('myproject')
        _tl.add_task('mytask')
        _t = _tl.get('mytask')
        self.failUnless(_t.position == _tl.count())

    def testMoveTask(self):
        """Move a task before another in project"""
        pass

    def testGloballyMoveTask(self):
        """Move a task before another globally"""
        pass

class TestOrgapp(unittest.TestCase):
    def testInit(self):
        """Test creating orgapp object 
        """
        O = Orgapp('/tmp/projects', ['unittest'])
        self.failUnless(O.projects_list == ['unittest'])

    def testAddTask(self):
        O = Orgapp('/tmp/projects', ['unittest'])
        O.add_task('test', 'unittest')
        self.failUnless(os.path.exists('/tmp/projects/unittest/tasks/test')



if __name__ == '__main__':
    unittest.main(verbosity=2)
