# -*- coding: utf8 -*-

class WellConfig():
    def __init__(self, index, avail, zcount, zslice, start):
        self.index = index
        self.avail = avail
        self.zcount = zcount
        self.zslice = zslice
        self.fileStart = start
        self.fileEnd = start + zcount

    def fileList(self):
        return [f'{i:05d}.jpg' for i in range(self.fileStart, self.fileEnd)]

class DishConfig():
    def __init__(self, index, config):
        self.index = index
        self.avail = int(config['Avail'])
        self.patientName = config['PatientName']
        self.pid = config['PID1']
        self.comment = config['Comment']
        self.reserve = config['Reserve']
        self.wells = []
        s = 1
        for i in range(1, 13):
            well_avail = int(config[f'Well{i}Avail'])
            zcount = int(config[f'Well{i}ZCount'])
            zslice = int(config[f'Well{i}ZSliceUm'])
            well_conf = WellConfig(i, well_avail, zcount, zslice, s)
            if well_conf.avail:
                self.wells.append(well_conf)
                s += zcount