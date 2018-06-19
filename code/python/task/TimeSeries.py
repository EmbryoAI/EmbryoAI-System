# -*- coding: utf8 -*-

from itertools import islice

class TimeSeries(object):
    def __init__(self):
        self.nf = self.next_frame_time()
        pass

    def __getitem__(self, slicing):
        tmp_serie = self.next_frame_time()
        if isinstance(slicing, int):
            return next(islice(tmp_serie, slicing, slicing+1))
        if isinstance(slicing, slice):
            return list(islice(tmp_serie, slicing.start, slicing.stop, slicing.step))
    
    def next(self):
        return next(self.nf)
    
    def move_to(self, index):
        self.nf = self.next_frame_time()
        next(islice(self.nf, index-1, index))

    def next_frame_time(self):
        d = 0
        h = 0
        m = 0
        yield '%d%02d%02d00' %(d, h, m)
        while True:
            m += 15
            dh, m = divmod(m, 60)
            h += dh
            dd, h = divmod(h, 24)
            d += dd
            yield '%d%02d%02d00' %(d, h, m)

def serie_to_time(timeserie):
    '''将一个timeserie转换为小时分钟tuple表示的时间'''
    if len(timeserie) != 7:
        raise TypeError('%s 不是一个TimeSerie格式' %timeserie)
    hour = int(timeserie[0])*24 + int(timeserie[1:3])
    minute = int(timeserie[3:5])
    return hour, minute

def serie_to_minute(timeserie):
    '''将一个timeserie转换为int的分钟数'''
    if len(timeserie) != 7:
        raise TypeError('%s 不是一个TimeSerie格式' %timeserie)
    return int(timeserie[0])*24*60 + int(timeserie[1:3])*60 + int(timeserie[3:5])

def serie_index_to_time(index):
    '''将一个timeserie序号转换为小时分钟tuple表示的时间'''
    return serie_to_time(TimeSeries()[index])

def serie_index_to_minute(index):
    '''将一个timeserie序号转换为int的分钟数'''
    return serie_to_minute(TimeSeries()[index])

def time_to_serie_index(hour, minute):
    '''将一个小时分钟的时间转换为timeserie序号'''
    return minute_to_serie_index(hour*60 + minute)

def minute_to_serie_index(minute):
    '''将一个int分钟数转换为timeserie序号'''
    return minute//15

def time_to_serie(hour, minute):
    '''将一个小时分钟的时间转换为timeserie'''
    return TimeSeries()[time_to_serie_index(hour, minute)]

def minute_to_serie(minute):
    '''将一个int分钟数转换为timeserie'''
    return TimeSeries()[minute_to_serie_index(minute)]

import unittest
class TsTest(unittest.TestCase):
    def test(self):
        ts = TimeSeries()
        self.assertEqual(ts[0], '0000000')
        self.assertEqual(ts[2], '0003000')
        self.assertEqual(ts[100], '1010000')
        self.assertEqual(ts[1:5], ['0001500', '0003000', '0004500', '0010000'])
        self.assertEqual(ts[:10:2], ['0000000', '0003000', '0010000', '0013000', '0020000'])
        self.assertEqual(ts.next(), '0000000')
        ts.move_to(100)
        self.assertEqual(ts.next(), '1010000')
        self.assertEqual(ts.next(), '1011500')
        self.assertEqual(serie_to_time('1010000'), (25, 0))
        self.assertEqual(serie_to_minute('1011500'), 1515)
        self.assertEqual(serie_index_to_time(101), (25, 15))
        self.assertEqual(serie_index_to_minute(100), 1500)
        self.assertEqual(time_to_serie_index(25, 15), 101)
        self.assertEqual(minute_to_serie_index(1500), 100)
        self.assertEqual(time_to_serie(25, 0), '1010000')
        self.assertEqual(minute_to_serie(1515), '1011500')

if __name__ == '__main__':
    unittest.main()
