from configparser import ConfigParser
import os

'''
读取INI配置文件帮助类
'''

class EmbryoIniParser(object):
    def __init__(self, path, encoding='Shift_JIS'):
        '''
        创建一个读取INI的对象
        @param path INI文件的完整路径
        @param encoding INI文件编码方式，默认为日文Shift_JIS
        '''
        if not (os.path.exists(path) and os.path.isfile(path)):
            raise ValueError("ini文件不存在")
        self.config = ConfigParser()
        self.config.read(path, encoding=encoding)
    def __getitem__(self, key):
        '''
        获取INI配置项
        @param key 配置项的键值
        '''
        return self.config[key]
    def section(self, key):
        return self.config[key]
    def value(self, section, name):
        return self.config[section][name]
    def __repr__(self):
        return str(self.config.__dict__)
    def __contains__(self, key):
        '''
        提供使用in操作符判断某个键值是否存在的方法
        @param key 配置项的键值
        '''
        return key in self.config
