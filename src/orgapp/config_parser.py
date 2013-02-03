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

from ConfigParser import SafeConfigParser
from os import path


class orgappConfigParser(SafeConfigParser):
    @staticmethod
    def get(section, key):
        candidates = ['config-dev.ini', 'config-stage.ini', 'config-prod.ini']
        full_path = path.dirname(__file__)
        parser = SafeConfigParser()
        for candidate in candidates:
            parser.read(path.join(full_path, '..', 'config', candidate))
            if parser.has_section(section) and parser.has_option(section, key):
                return parser.get(section, key)


def configure(cls):
    origin_init = cls.__init__

    def __init__(self, parser=None, *args, **kws):
        if not parser:
            parser = orgappConfigParser()
            self.path = parser.get('tasks', 'path')
            self.repo = parser.get('repo', 'repo')
            self.cache_path = parser.get('doc', 'cache')
        if not parser.has_section('tasks'):
            parser.add_section('tasks')
        if not parser.has_section('doc'):
            parser.add_section('doc')
        if not parser.has_section('repo'):
            parser.add_section('repo')
        try:
            self.path = parser.get('tasks', 'path')
        except:
            parser.set('tasks', 'path', '../tasks.db')
            self.path = parser.get('tasks', 'path')
        try:
            self.cache_path = parser.get('doc', 'cache')
        except:
            parser.set('doc', 'cache', '/tmp/cache')
            self.cache_path = parser.get('doc', 'cache')
        try:
            self.doc = parser.get('doc', 'doc')
        except:
            parser.set('doc', 'doc', 'doc')
            self.doc = parser.get('doc', 'doc')
        try:
            self.repo_root = parser.get('repo', 'repo_root')
        except:
            parser.set('repo', 'repo_root', 'None')
            self.repo_type = parser.get('repo', 'repo_root')
        try:
            self.git_repos = parser.get('repo', 'git_repos').split(',')
        except:
            self.git_repos = None
        try:
            self.hg_repos = parser.get('repo', 'hg_repos').split(',')
        except:
            self.hg_repos = None
        origin_init(self, *args, **kws)

    cls.__init__ = __init__
    return cls
