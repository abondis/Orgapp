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

from orgapp.model import Statuses
from orgapp.project import Project
from orgapp.model import Tasks
from orgapp.model import Projects
from config_parser import configure
import os


@configure
class Orgapp:
    """A bunch of projects and a global Tasklist
    """
    def __init__(
            self,
            statuses=[]):
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

    def add_task(self, name, status, description, project, filetype='md'):
        p = self.projects[project]
        p.create_task(name, status, description, filetype)

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

    def set_title(self, tid, new_title):
        """ Set tasks #tid with new_status"""
        _t = Tasks.get(id=tid)
        # get old title
        _old_title = _t.name
        # move/rename file
        _p = self.projects[_t.project.name]
        #TODO: define in project.py
        _p.rename_file(old_name=_old_title, new_name=new_title,
                       in_path='tasks')
        _t.rename(new_title)
        _t.save()

    def delete(self, tid):
        """ Deletes a task """
        _t = Tasks.get(id=tid)
        _t.delete_instance()
        #TODO recalculate the order of all the tasks

    def set_description(self, tid, new_description):
        """ Set tasks #tid with new_status"""
        _t = Tasks.get(id=tid)
        # get task title
        # and project ?
        # save file's content/description
        _t.set_description(new_description)
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


o = Orgapp(
    statuses=['backlog', 'new', 'running', 'done'])
