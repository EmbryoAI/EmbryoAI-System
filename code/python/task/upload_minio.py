# -*- coding: utf8 -*-

from task.TimeSeries import TimeSeries, serie_to_minute
import os
import json
from app import conf,minioClient

def upload_dish(path, dish_info):
    '''
    处理一个皿目录方法
        @param path: 采集目录完整路径
        @param dish_info: DishConfig配置信息对象
        @returns state: 皿结束采集标志 True - 已结束采集；False - 未结束采集
    '''
    from functools import partial
    dish_path = path + f'DISH{dish_info.index}' + os.path.sep # 皿目录完整路径
    if not dish_info.lastSerie:
        last_op = '0' * 7
    else:
        
        last_op = TimeSeries()[serie_to_minute(dish_info.lastSerie)//15+1]
    # 已经处理过的时间序列列表
    processed = TimeSeries().range(last_op)
    # 以下两行代码使用偏函数从当前目录中得到所有合法且未处理的时间序列子目录
    f = partial(dir_filter, processed=processed, base=dish_path)
    todo = list(sorted(filter(f, os.listdir(dish_path))))


    for serie in todo:
        # 交给process_serie_dir模块对时间序列目录进行处理
        last_op = process_serie(dish_path, serie, dish_info)
        # 每次处理完成都将最新处理的时间序列目录回写到state对象中
        dish_info.lastSerie = last_op
    # 返回皿目录是否已经结束采集的标志
    return check_finish_state(path, last_op)

def check_finish_state(path, last_serie):
    '''
    检查皿目录状态是否已经结束采集，判断标准为当前系统时间是否已经超过最后一次采集的时间序列一个小时
        @param path: 采集目录的完整路径，为了读取DishInfo.ini文件
        @param last_serie: 最后处理完成的时间序列目录名称
        @returns state: True - 结束采集；False - 未结束采集
    '''
    import datetime as dt
    from task.ini_parser import EmbryoIniParser
    ini_conf = EmbryoIniParser(path+'DishInfo.ini')
    start_ = ini_conf['Timelapse']['StartTime'] 
    start_time = dt.datetime.strptime(start_, '%Y%m%d%H%M%S') # 采集开始时间
    end_time = start_time + dt.timedelta(minutes=serie_to_minute(last_serie)) # 结束采集时间
    now = dt.datetime.now() # 当前系统时间
    interval = now - end_time
    if interval.days > 0 or interval.seconds > conf['ACTIVE_TIMEOUT']:
        return True # 大于设定时间，返回True
    return False


def dir_filter(path, processed, base):
    '''
    过滤器方法，滤掉非子目录、已经处理过的目录以及focus缩略图目录
        @param path: 子目录名称
        @param processed: 已经处理过的目录列表
        @param base: 皿目录完整路径
    '''
    if not os.path.isdir(base + path):
        return False
    if path in processed:
        return False
    if path == 'focus':
        return False
    return True