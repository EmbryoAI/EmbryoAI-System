from configparser import ConfigParser

class EmbryoIniParser(object):
    def __init__(self, path, encoding='Shift_JIS'):
        self.config = ConfigParser()
        self.config.read(path, encoding=encoding)
    def __getitem__(self, key):
        return self.config[key]
    def section(self, key):
        return self.config[key]
    def value(self, section, name):
        return self.config[section][name]
    def __repr__(self):
        return str(self.config.__dict__)
    def __contains__(self, key):
        return key in self.config
