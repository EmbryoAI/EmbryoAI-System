# -*- coding: utf8 -*-

from itertools import islice
from common import getdefault

'''
时间序列辅助类TimeSeries及辅助工具方法
'''

class TimeSeries(object):
    def __init__(self):
        '''创建一个TimeSeries对象'''
        self.nf = self.next_frame_time()

    def __getitem__(self, slicing):
        '''
        提供slice方法访问TimeSeries
            @param slicing: int/slice，slice参数
            @returns TimeSeries: str/list，单个的TimeSeries对象字符串或多个TimeSeries对象列表
        可以使用python方括号方式slice时间序列，如ts[0:3] -> ['0000000','0001500','0003000']
        '''
        tmp_serie = self.next_frame_time()
        if isinstance(slicing, int):
            return next(islice(tmp_serie, slicing, slicing+1))
        if isinstance(slicing, slice):
            return list(islice(tmp_serie, slicing.start, slicing.stop, slicing.step))
    
    def next(self):
        '''获取下一个时间序列'''
        return next(self.nf)
    
    def move_to(self, index):
        '''将时间序列移动到某个位置'''
        self.nf = self.next_frame_time()
        next(islice(self.nf, index-1, index))
    
    def range(self, *kargs, **kwargs):
        '''
        提供类似range的方法获取TimeSeries的一段连续区域
            @param begin: 开始位置（包含），省略默认为0
            @param end: 结束位置（不包含）
            @param step: 步长，省略默认为15（分钟）
            @returns series: TimeSeries列表
        '''
        begin = getdefault(kwargs, 'begin', '0000000')
        end = getdefault(kwargs, 'end', '0000000')
        step = getdefault(kwargs, 'step', 15)
        if len(kargs) == 1:
            end = kargs[0]
        if len(kargs) == 2:
            begin = kargs[0]
            end = kargs[1]
        if len(kargs) == 3:
            begin = kargs[0]
            end = kargs[1]
            step = kargs[2]
        if len(begin) != 7 or len(end) != 7 or step%15 != 0:
            raise ValueError('Wrong begin, end or step param. Begin, end should '
                'be 7 digits string. Step should be multiple of 15 integer')
        tominute = lambda x: int(x[0])*24*60 + int(x[1:3])*60 + int(x[3:5])
        bindex = tominute(begin)//15
        eindex = tominute(end)//15
        k = step//15
        return self.__getitem__(slice(bindex, eindex, k))

    def next_frame_time(self):
        '''计算下一个时间序列字符串的辅助方法'''
        d = 0
        h = 0
        m = 0
        yield f'{d:d}{h:02d}{m:02d}00'
        while True:
            m += 15
            dh, m = divmod(m, 60)
            h += dh
            dd, h = divmod(h, 24)
            d += dd
            yield f'{d:d}{h:02d}{m:02d}00'

def serie_to_time(timeserie):
    '''
    将一个timeserie转换为小时分钟tuple表示的时间
        @param timeserie: 7为数字组成的字符串表示的时间序列
        @returns hour, minute: 小时数和分钟数的元组
    '''
    if len(timeserie) != 7:
        raise TypeError('%s 不是一个TimeSerie格式' %timeserie)
    hour = int(timeserie[0])*24 + int(timeserie[1:3])
    minute = int(timeserie[3:5])
    return hour, minute

def serie_to_minute(timeserie):
    '''
    将一个timeserie转换为int的分钟数
        @param timeserie: 7为数字组成的字符串表示的时间序列
        @returns minutes: 分钟数
    '''
    if len(timeserie) != 7:
        raise TypeError('%s 不是一个TimeSerie格式' %timeserie)
    return int(timeserie[0])*24*60 + int(timeserie[1:3])*60 + int(timeserie[3:5])

def serie_index_to_time(index):
    '''
    将一个timeserie序号转换为小时分钟tuple表示的时间
        @param index: 时间序列的序号
        @returns hour, minute: 小时数和分钟数的元组
    '''
    return serie_to_time(TimeSeries()[index])

def serie_index_to_minute(index):
    '''
    将一个timeserie序号转换为int的分钟数
        @param index: 时间序列的序号
        @returns minutes: 分钟数
    '''
    return serie_to_minute(TimeSeries()[index])

def time_to_serie_index(hour, minute):
    '''
    将一个小时分钟的时间转换为timeserie序号
        @param hour: 小时数
        @param minute: 分钟数
        @returns index: 时间序列序号
    '''
    return minute_to_serie_index(hour*60 + minute)

def minute_to_serie_index(minute):
    '''
    将一个int分钟数转换为timeserie序号        
        @param minute: 分钟数
        @returns index: 时间序列序号 
    '''
    return minute//15

def time_to_serie(hour, minute):
    '''
    将一个小时分钟的时间转换为timeserie
        @param hour: 小时数
        @param minute: 分钟数
        @returns serie: 时间序列字符串
    '''
    return TimeSeries()[time_to_serie_index(hour, minute)]

def minute_to_serie(minute):
    '''
    将一个int分钟数转换为timeserie
        @param minute: 分钟数
        @returns serie: 时间序列字符串
    '''
    return TimeSeries()[minute_to_serie_index(minute)]

'''以下是单元测试'''
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
        self.assertEqual(len(ts.range('0010000')), 4)
        self.assertEqual(len(ts.range('0100000', '0123000')), 10)
        self.assertEqual(len(ts.range('1000000', '2000000', 60)), 24)
        self.assertEqual(len(ts.range(begin='0011500', end='1013000')), 97)
        self.assertEqual(len(ts.range(begin='0000000', end='4184500', step=120)), 58)

if __name__ == '__main__':
    unittest.main()
