from ConfigParser import SafeConfigParser


class orgappConfigParser():
    @staticmethod
    def get(section, key):
        candidates = ['config-dev.ini', 'config-stage.ini', 'config-prod.ini']
        parser = SafeConfigParser()
        for candidate in candidates:
            parser.read(candidate)
            if parser.has_section(section) and parser.has_option(section, key):
                return parser.get(section, key)
