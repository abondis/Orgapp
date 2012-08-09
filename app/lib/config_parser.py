#!/usr/bin/env python
#-=- encoding: utf-8 -=-
from ConfigParser import SafeConfigParser, NoSectionError
from os import path


class orgappConfigParser():
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
    #donc on passe un configparser
    #s'il y en a pas il essaie de loader le defaut
    origin_init = cls.__init__

    def __init__(self, parser=None, *args, **kws):
        if not parser:
            parser = orgappConfigParser()
            self.path = parser.get('tasks', 'path')
            if not self.path:
            #s'il y a pas les settings il les définit par défaut
                try:
                    parser.set('tasks', 'path', 'tasks.db')
                except NoSectionError:
                    # Create non-existent
                    # section
                    parser.add_section('tasks')
                    parser.set('tasks', 'path', 'tasks.db')
                self.path = parser.get('tasks', 'path')
        else:
            self.path = parser.get('tasks', 'path')
        origin_init(self, *args, **kws)

    cls.__init__ = __init__
    return cls
