#!/usr/bin/env python
#-=- encoding: utf-8 -=-
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
