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

from orgapp.model import Tasks
from orgapp.model import Projects
import datetime
from hashlib import md5


class Tasklist:
    """A tasklist handling Tasks from the DB
    and setting values like: md5hash, position"""
    def __init__(self, project='*'):
        if project == '*':
            self.tasks = Tasks.select()
            #self.project = Projects.get_or_create(name)
        else:
            self.project = Projects.get_or_create(name=project)
            self.tasks = Tasks.select().where(Tasks.project == self.project)

    def count(self):
        return Tasks.select().count()

    def get(self, name):
        q = Tasks.get(Tasks.name == name, Tasks.project == self.project)
        return q

    def add_task(self, name, status):
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
