#
#This file is part of Orgapp.
#
#Orgapp is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Orgapp is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Orgapp.  If not, see <http://www.gnu.org/licenses/>.

from orgapp.repo import Repo
from orgapp.model import Statuses
from orgapp.model import Projects
from orgapp.doc import Doc
from orgapp.model import Tasks
from hashlib import md5
import datetime


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

    def create_task(self, name, status, description='', MU_type='md'):
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
        _t.project = Projects.get_or_create(name=self.name)
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
