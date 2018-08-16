# -*- coding: utf8 -*-

'''
皿配置信息类 DishConfig
孔配置信息类 WellConfig
'''

class WellConfig():
    ''' 孔的配置信息，数据从INI配置文件中获得'''
    def __init__(self, d=None):
        if d:
            self.__dict__.update(d)
            self.series = {}
            for s in d['series']:
                self.series[s] = SerieInfo(d['series'][s])
    def wellSetup(self, index, avail, zcount, zslice, start):
        self.index = index # 孔序号 1-12
        self.avail = avail # 是否有效标志 0 - 无效 1 - 有效
        self.zcount = zcount # Z轴层数，即垂直方向采集图像的张数，最大19
        self.zslice = zslice # Z轴每层距离，单位um
        self.fileStart = start # 孔图像开始序号，包含
        self.fileEnd = start + zcount # 空图像结束序号，不包含
        self.zIndexFiles = self.fileList() # Z轴序号与图像文件对照字典，从1开始
        self.lastEmbryoSerie = None # 最后一个能定位到胚胎的时间序列值
        self.series = {} # 该孔的所有时间序列

    def fileList(self):
        '''获取孔的所有Z轴序号与采集图像文件名称对照字典表'''
        return {i-self.fileStart+1: f'{i:05d}.jpg' for i in range(self.fileStart, self.fileEnd)}
    
    def addSerie(self, frame):
        self.series[frame.serie] = frame

class DishConfig():
    '''皿的配置信息，数据从INI配置文件中获得'''
    def __init__(self, d=None):
        if d:
            self.__dict__.update(d)
            self.wells = {}
            for w in d['wells']:
                self.wells[w] = WellConfig(d['wells'][w])

    def dishSetup(self, index, config, well_count, incubator_name):
        self.index = index # 皿序号 1-9
        self.avail = int(config['Avail']) # 是否有效标志 0 - 无效 1 - 有效
        self.incubatorName = incubator_name
        self.patientName = config['PatientName'] # 在采集软件中登记的病人姓名，无法登记中文，因为编码为日文Shift_JIS
        self.pid = config['PID1'] # 在采集软件中登记的病人ID
        self.comment = config['Comment'] # 在采集软件中登记的备注
        self.reserve = config['Reserve'] # 在采集软件中登记的保留字段
        self.lastSerie = None # 目前皿目录中最后一个时间序列
        self.finished = False # 皿处理完成标记
        self.wells = {} # 皿的孔列表，此处未必是1-12，仅保存avail为1的孔至此列表
        s = 1 # 图像序号，从1开始
        for i in range(1, well_count+1):
            well_avail = int(config[f'Well{i}Avail'])
            zcount = int(config[f'Well{i}ZCount'])
            zslice = int(config[f'Well{i}ZSliceUm'])
            well_conf = WellConfig()
            well_conf.wellSetup(i, well_avail, zcount, zslice, s)
            if well_conf.avail:
                self.wells[i] = well_conf # 当avail为1时，将孔加到wells列表中
                s += zcount # 图像序号每次增加Z轴图像数

class SerieInfo():
    def __init__(self, d=None):
        if d:
            self.__dict__.update(d)

    def serieSetup(self, wellConfig, serie):
        from app import conf
        self.serie = serie # 序列号，7位数字，DHHmmss
        self.embryoFound = False # 是否自动找到胚胎的标志
        self.sharp = f'{(wellConfig.fileStart + wellConfig.fileEnd) // 2:05d}.jpg' # 清晰图文件名，默认序号处于中间位置的一张
        self.focus = conf['NO_EMBRYO_IMAGE_URL'] # 缩略图文件路径，默认为未找到胚胎的图像URL
        self.stage = None # 胚胎所处阶段，自动分类得到的所属阶段
        self.outerArea = None # 胚胎外周面积，单位um2
        self.outerDiameter = None # 胚胎外周直径，单位um
        self.innerArea = None # 胚胎内细胞面积，单位um2
        self.innerDiameter = None # 胚胎内细胞直径，单位um
        self.zonaThickness = None # 透明带厚度，单位um
        self.expansionArea = None # 扩张囊腔面积，单位um2


import unittest

class ConfigTest(unittest.TestCase):
    def test(self):
        import json
        file = '/Users/wangying/git/repos/EmbryoAI-System/code/captures/20180422152100/DISH8/dish_state.json'
        with open(file) as fn:
            jdict = json.load(fn)
        dc = DishConfig(jdict)
        self.assertEqual(len(dc.wells), 3)
        self.assertEqual(len(dc.wells['1'].series), 673)

if __name__=='__main__':
    unittest.main()
