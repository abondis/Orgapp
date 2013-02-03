#!/usr/bin/env python
#-=- encoding: utf-8 -=-
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


from peewee import SqliteDatabase, Model, CharField, TextField, DateTimeField
from peewee import ForeignKeyField, IntegerField, FloatField
import datetime
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
#DEFAULTSTATUS = 'new'
#DEFAULTPROJECT = 'unknown'
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
        related_name='tasks')
    status = ForeignKeyField(
        Statuses,
        related_name='tasks')
    # FIXME: how to use Tasks.count for this field ?
    position = IntegerField(default=0)
    time = FloatField(default=0)

    class Meta:
        """ Default order_by """
        order_by = ('position',)

    def rename(self, new_name):
        """Rename a task"""
        if new_name == '':
            new_name = 'No name'

        self.name = new_name
        self.save()

    def set_description(self, new_description):
        """ Change the description of the task"""
        if new_description == '':
            new_description = 'No description'

        self.description = new_description
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

#Projects.get_or_create(name='unknown')
#Statuses.get_or_create(name='new')


#http://peewee.readthedocs.org/en/latest/peewee/cookbook.html#creating-a-database-connection-and-tables
