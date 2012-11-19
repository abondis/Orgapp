#!/usr/bin/env python
#-=- encoding: utf-8 -=-
from peewee import *
import datetime
from hashlib import md5
"""
Maybe use peewee instead of macaron?
Model
-----
- Tasks:
    - name
    - md5
    - creation date
    - last modification
    - project
    - status
    - position
- Projects:
    - id
    - name
- Statuses:
    - id
    - name
"""

tasks_db = SqliteDatabase('tasks.db')
DEFAULTSTATUS = 'new'
DEFAULTPROJECT = 'unknown'
tasks_db.connect()


class CustomModel(Model):
    class Meta:
        database = tasks_db

class Projects(CustomModel):
    name = CharField()


class Statuses(CustomModel):
    name = CharField()

try:
    Projects.create_table()
except:
    pass
try:
    Statuses.create_table()
except:
    pass


class Tasks(CustomModel):
# not null is forced by default
    name = CharField()
    # FIXME: how to generate the md5 automatically ?
    md5hash = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)
    last_modification = DateTimeField(default=datetime.datetime.now)
    project = ForeignKeyField(
            Projects,
            related_name='tasks',
            default = Projects.get_or_create(name=DEFAULTPROJECT))
    status = ForeignKeyField(
            Statuses,
            related_name='tasks',
            default = Statuses.get_or_create(name=DEFAULTSTATUS))
    # FIXME: how to use Tasks.count for this field ?
    position = IntegerField(default=-1)

    class Meta:
        """ Default order_by """
        order_by = ('position',)

    def rename(self, new_name):
        """Rename a task"""
        self.name=new_name
        self.save()

    def get_all(self):
        """ get all tasks """
        return self.select()

    def for_project(self, project_name):
        """ get tasks grouped by statuses for specific project """
        #_p = Projects.get(Projects.name == project_name)
        return self.select(Projects.name == project_name)


try:
    Tasks.create_table()
except:
    pass

Projects.get_or_create(name='unknown')
Statuses.get_or_create(name='new')


#http://peewee.readthedocs.org/en/latest/peewee/cookbook.html#creating-a-database-connection-and-tables



"""
Objects
-------
- Tasklist(Project='*'):
    - Model.Tasks.filter_by(Project)
        .order_by(Model.Tasks.position)
        .group_by(Model.Statuses)
- Project:
    - Tasklist
    - Repo(config.path, config.type)
    - Documents(Repo, Type)
- Documents:
    - path
    - render
    - cache
    - create/modify
- Repo:
    - Type
    - Path
    - commit
- Orgapp:
    - Tasklist('*')
    - Projects([config.projects])
"""
import mercurial.commands as hg
from mercurial import ui as hgui, localrepo as hgrepo
from dulwich import repo as gitrepo
import os

class Repo:
    def __init__(self, path, vcs_type):
        self.ui = hgui.ui()
        self.path = path
        self.vcs_type = vcs_type
        if self.vcs_type == 'git':
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            try:
                self.r = gitrepo.Repo(self.path)
            except:
                self.r = gitrepo.Repo.init(self.path)
        elif self.vcs_type == 'hg':
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            try:
                self.r = hgrepo.localrepository(
                                        self.ui,
                                        self.path)
            except:
                hg.init(self.ui, self.path)
                self.r = hgrepo.localrepository(
                        self.ui,
                        self.path)
    def add_file(self, path):
        if self.vcs_type == 'git':
            # git wants a relative path
            path = path[len(self.path)+1:]
            self.r.stage(path)
        # FIXME: does not work if there was an
            # issue with other uncommitted things
            self.r.do_commit(
                message='commit {0}'.format(path))
        elif self.vcs_type == 'hg':
            hg.add(self.ui, self.r, path)
            hg.commit(
                self.ui,
                self.r,
                path,
                message='commit {0}'.format(path))

class Project:
    def __init__(
            self,
            name,
            path,
            vcs_type,
            cache_path = '/tmp',
            doc_path='doc',
            tasks_path='tasks'):
        self.name = name
        # root path
        self.path = path
        # repo's path
        self.fullpath = path + '/' + self.name
        # root cache path
        self.cache_path = cache_path + '/' + self.name
        # doc's path relative to repo's path
        self.doc_path = doc_path
        # tasks's path relative to repo's path
        self.tasks_path = tasks_path
        # vcs type: git or hg
        self.vcs_type = vcs_type
        # path to cache tasks
        self.tasks_cache = self.cache_path + '/' + self.tasks_path
        # path to cache doc
        self.doc_cache = self.cache_path + '/' + self.doc_path
        # open project's repo
        self.r = Repo(self.fullpath, self.vcs_type)
        # project's documents full path
        self.doc_fullpath = self.fullpath+'/'+self.doc_path
        # tasks's documents full path
        self.tasks_fullpath = self.fullpath+'/'+self.tasks_path
        # project's documents handler
        self.doc_files = Doc(self.doc_fullpath, self.doc_cache)
        # tasks's documents handler
        self.tasks_files = Doc(self.tasks_fullpath, self.tasks_cache)

    def create_task(self, name):
        _t = Tasks()
        _d = str(datetime.datetime.now())
        _t.name = name
        _t.md5hash = md5(_d+name)
        _t.save()


import markdown as md
class Doc:
    """Handle documents"""
    def __init__(self, root_path, cache_path):
        self.renderers = {'copy': self.render_copy, 'md': self.render_md}
        self.root_path = root_path
        self.cache_path = cache_path
        ## create doc dir
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        # create doc cache dir
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    def get_file_ext(self, path):
        return path.rsplit('.')[-1]

    def create_doc(self, filename, content, mode='doc'):
        """ creates a document using some content
        mode: is doc by default, can be cache to use the cache_path instead
        of root_path
        """
        if mode == 'doc':
            path = self.root_path
        elif mode == 'cache':
            path = self.cache_path
        with open(path+'/'+filename, 'w') as _f:
            _f.write(content)

    def cache(self, filename):
        content = self.render(filename)
        self.create_doc(filename, content, mode='cache')

    def render(self, filename):
        """renders a doc into cache_path.
        Let project handle path construction"""
        _ext = self.get_file_ext(filename)
        if _ext not in self.renderers.keys():
            _ext = 'copy'
        with open(self.root_path+'/'+filename, 'r') as _f:
            content = _f.read()
            return(self.renderers[_ext](content))

    def render_copy(self, content):
        return content

    def render_md(self, content):
        return(md.markdown(content, ['fenced_code', 'tables', 'codehilite']))


