#!/usr/bin/env python
#-=- encoding: utf-8 -=-
from peewee import SqliteDatabase, Model, CharField, DateTimeField
from peewee import ForeignKeyField, IntegerField, FloatField
import datetime
from hashlib import md5
from config_parser import configure
"""
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
    - time
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
    """Newly created task gets the highest
    position of all tasks (least important)
    Moving tasks will be relative to project, using positions available in
    the project
    """
# not null is forced by default
    name = CharField()
    description = TextField(null=True)
    # FIXME: how to generate the md5 automatically ?
    md5hash = CharField()
    created_date = DateTimeField(default=datetime.datetime.now)
    last_modification = DateTimeField(default=datetime.datetime.now)
    project = ForeignKeyField(
        Projects,
        related_name='tasks',
        default=Projects.get_or_create(name=DEFAULTPROJECT))
    status = ForeignKeyField(
        Statuses,
        related_name='tasks',
        default=Statuses.get_or_create(name=DEFAULTSTATUS))
    # FIXME: how to use Tasks.count for this field ?
    position = IntegerField(default=0)
    time = FloatField(default=0)

    class Meta:
        """ Default order_by """
        order_by = ('position',)

    def rename(self, new_name):
        """Rename a task"""
        self.name = new_name
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
            path = path[len(self.path) + 1:]
            self.r.stage(path)
        # FIXME: does not work if there was an
            # issue with other uncommitted things
            self.r.do_commit(
                message='commit {0}'.format(path))
        elif self.vcs_type == 'hg':
            #_lock = self.r.lock()
            print '=' * 35
            print self.r
            print path
            print '=' * 35
            hg.add(self.ui, self.r, path)
            hg.commit(
                self.ui,
                self.r,
                path,
                message='commit {0}'.format(path))
            #_lock.release()


class Project:
    def __init__(
            self,
            name,
            path,
            vcs_type,
            cache_path='/tmp',
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
        self.doc_fullpath = self.fullpath + '/' + self.doc_path
        # tasks's documents full path
        self.tasks_fullpath = self.fullpath + '/' + self.tasks_path
        # project's documents handler
        self.doc_files = Doc(self.doc_fullpath, self.doc_cache)
        # tasks's documents handler
        self.tasks_files = Doc(self.tasks_fullpath, self.tasks_cache)
        # create project in db if not exist
        Projects.get_or_create(name=self.name)

    def create_task(self, name, description='', MU_type='md', status=DEFAULTSTATUS):
        """MarkUp type defaults to 'markdown'
        """
        _status = Statuses.get(name=status)
        _t = Tasks()
        _d = str(datetime.datetime.now())
        _t.name = name
        _t.description = description
        _t.status = _status
        _t.md5hash = md5(_d + name)
        _t.position = Tasks.select().where(Tasks.status == _status).count()
        _t.save()

        # TODO save task on disk, inside the repo
        #if description == '':
            #description = name
        #self.tasks_files.create_doc(name+'.'+MU_type, description)
        #self.tasks_files.create_doc(name, description)
        #self.r.add_file(self.r.path+'/tasks/'+name)
        print '*' * 100
        print self.tasks_files.root_path
        print 'tasks fullpath: ' + self.tasks_fullpath + '/' + name + '.'\
            + MU_type
        print '*' * 100
        #self.r.add_file(self.tasks_fullpath+'/'+name+'.'+MU_type)

    def create_doc(self, name, content='', MU_type='md'):
        self.doc_files.create_doc(name + '.' + MU_type, content)
        self.r.add_file(self.doc_fullpath + '/' + name + '.' + MU_type)
        self.doc_files.cache(name + '.' + MU_type)


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

    def get_doc(self, filename):
        with open(self.cache_path + '/' + filename) as _f:
            return _f.read()

    def create_doc(self, filename, content, mode='doc'):
        """ creates a document using some content
        mode: is doc by default, can be cache to use the cache_path instead
        of root_path
        """
        if mode == 'doc':
            path = self.root_path
        elif mode == 'cache':
            path = self.cache_path
        with open(path + '/' + filename, 'w') as _f:
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
        with open(self.root_path + '/' + filename, 'r') as _f:
            content = _f.read()
            return(self.renderers[_ext](content))

    def render_copy(self, content):
        return content

    def render_md(self, content):
        return(md.markdown(content, ['fenced_code', 'tables', 'codehilite']))


class Tasklist:
    """A tasklist handling Tasks from the DB
    and setting values like: md5hash, position"""
    def __init__(self, project='*'):
        if project == '*':
            self.tasks = Tasks.select()
            self.project = Projects.get_or_create(name=DEFAULTPROJECT)
        else:
            self.project = Projects.get_or_create(name=project)
            self.tasks = Tasks.select().where(Tasks.project == self.project)

    def count(self):
        return Tasks.select().count()

    def get(self, name):
        q = Tasks.get(Tasks.name == name, Tasks.project == self.project)
        return q

    def add_task(self, name, status=DEFAULTSTATUS):
        _now = str(datetime.datetime.now())
        _md5hash = md5(_now + name).hexdigest()
        _pos = self.count() + 1
        Tasks.create(
            name=name,
            md5hash=_md5hash,
            project=self.project,
            position=_pos)

    def move(self, source, dest):
        pass


@configure
class Orgapp:
    """A bunch of projects and a global Tasklist
    """
    def __init__(
            self,
            statuses=[DEFAULTSTATUS]):
        for s in statuses:
            Statuses.get_or_create(name=s)
        #self.root_path = root_path
        #self.projects_list = projects_list
        self.projects = {}
        for _p in self.hg_repos:
            self.projects[_p] = Project(_p, self.repo_root, 'hg')
        for _p in self.git_repos:
            self.projects[_p] = Project(_p, self.repo_root, 'git')

    def count_tasks_by_status(self, tid):
        _s = Tasks.get(id=tid).status
        return Tasks.select().where(Tasks.status == _s).count()

    def __getitem__(self, item):
        return self.projects[item]

    def add_task(self, name, description, project, content=None, status=DEFAULTSTATUS):
        if not content:
            content = name
        p = self.projects[project]
        p.create_task(name, description, content, status=status)

    def set_position(self, tid, new_pos, project='*'):
        """Set new position and update their friends"""
        if Tasks.select().count() == 1:
            return
        _t = Tasks.get(id=tid)
        # FIXME: why a str?
        old_pos = str(_t.position)
        # query to select tasks to update
        updq = Tasks.select().where(Tasks.status == _t.status)
        # update all Tasks
        # update tasks in the specific project
        if not project == '*':
            updq = updq.where(
                Tasks.project == Projects.get(name=project))
        # update from top to bottom
        if int(new_pos) > int(old_pos):
            updq = updq.where(Tasks.position <= str(new_pos),
                              Tasks.position >= str(old_pos))
        # update from bottom to top
        else:
            updq = updq.where(Tasks.position >= str(new_pos),
                              Tasks.position <= str(old_pos))
            updq = updq.order_by(Tasks.position.desc())
        # FIXME: hackish, find if there is a better way
        prev = [x for x in updq.limit(1)][0]
        updq = updq.limit(-1).offset(1)
        _first = prev
        if updq.count() > 0:
            print 'updq.count: ' + str(updq.count())
            print 'updq' + str([x.id for x in updq])
            prev_pos = prev.position
            for upd_t in updq:
                next_pos = upd_t.position
                print "moving task: " + str(upd_t.id) + " from: " +\
                    str(next_pos) + " to: " + str(prev_pos)
                upd_t.position = prev_pos
                upd_t.save()
                prev_pos = next_pos
        _first.position = new_pos
        _first.save()

    def force_position(self, tid, new_pos):
        _t = Tasks.get(id=tid)
        _t.position = new_pos
        _t.save()

    def set_status(self, tid, new_status):
        """ Set tasks #tid with new_status"""
        _t = Tasks.get(id=tid)
        _s = Statuses.get(name=new_status)
        _t.status = _s
        _t.save()

    def align_status(self, status):
        """ Aligns tasks in specific status to position 0"""
        _t = Tasks.select().where(Tasks.status.name == status)
        _t = _t.order_by(Tasks.position.desc())
        _count = _t.count()
        for x in _t:
            x.position = _count
            x.save()
            _count -= 1

    def count(self):
        return Tasks.select().count()
