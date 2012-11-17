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
            print dir(self.r)
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

