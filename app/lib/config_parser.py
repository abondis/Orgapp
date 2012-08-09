from ConfigParser import SafeConfigParser
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
