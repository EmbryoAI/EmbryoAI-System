# -*- coding: utf8 -*-

'''
皿配置信息类 DishConfig
孔配置信息类 WellConfig
'''

class WellConfig():
    ''' 孔的配置信息，数据从INI配置文件中获得'''
    def __init__(self, index, avail, zcount, zslice, start):
        self.index = index # 孔序号 1-12
        self.avail = avail # 是否有效标志 0 - 无效 1 - 有效
        self.zcount = zcount # Z轴层数，即垂直方向采集图像的张数，最大19
        self.zslice = zslice # Z轴每层距离，单位um
        self.fileStart = start # 孔图像开始序号，包含
        self.fileEnd = start + zcount # 空图像结束序号，不包含

    def fileList(self):
        '''获取孔的所有采集图像文件名称列表'''
        return [f'{i:05d}.jpg' for i in range(self.fileStart, self.fileEnd)]

class DishConfig():
    '''皿的配置信息，数据从INI配置文件中获得'''
    def __init__(self, index, config):
        self.index = index # 皿序号 1-9
        self.avail = int(config['Avail']) # 是否有效标志 0 - 无效 1 - 有效
        self.patientName = config['PatientName'] # 在采集软件中登记的病人姓名，无法登记中文，因为编码为日文Shift_JIS
        self.pid = config['PID1'] # 在采集软件中登记的病人ID
        self.comment = config['Comment'] # 在采集软件中登记的备注
        self.reserve = config['Reserve'] # 在采集软件中登记的保留字段
        self.wells = [] # 皿的孔列表，此处未必是1-12，仅保存avail为1的孔至此列表
        s = 1 # 图像序号，从1开始
        for i in range(1, 13):
            well_avail = int(config[f'Well{i}Avail'])
            zcount = int(config[f'Well{i}ZCount'])
            zslice = int(config[f'Well{i}ZSliceUm'])
            well_conf = WellConfig(i, well_avail, zcount, zslice, s)
            if well_conf.avail:
                self.wells.append(well_conf) # 当avail为1时，将孔加到wells列表中
                s += zcount # 图像序号每次增加Z轴图像数