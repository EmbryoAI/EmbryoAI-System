from configparser import ConfigParser

class EmbryoIniParser(object):
    def __init__(self, path, encoding='utf-8'):
        self.config = ConfigParser()
        self.config.read(path, encoding=encoding)
    def __getitem__(self, key):
        return self.config[key]
    def section(self, key):
        return self.config[key]
    def value(self, section, name):
        return self.config[section][name]

path = '/Users/wangying/git/repos/EmbryoAI-System/models/demo0/20170624151700/DishInfo.ini'
c = EmbryoIniParser(path, 'Shift_JIS')
print(c['Timelapse']['StartTime'])