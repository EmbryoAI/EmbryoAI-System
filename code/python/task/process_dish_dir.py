# -*- coding: utf8 -*-

from task.TimeSeries import TimeSeries, serie_to_minute
import os
import json
import re
from app import app, conf
from task.process_serie_dir import process_serie

import logUtils as logger

'''
### 皿目录处理模块，皿目录命名规则：天小时分钟秒数 即 DHHmmss，后两位都为0，参见TimeSeries辅助类
#### 处理需要完成的工作包括：
- 为避免重复处理某个时间，读取LAST_SERIE_FILENAME配置的文件获得最后处理的时间目录（已完成，但后续可能要修改该文件为JSON格式）
- 处理所有未处理的时间目录，时间目录的处理逻辑交给process_serie_dir模块（已完成）
- 处理完所有未处理的目录后，检查最后一次的采集时间与当前系统时间相差是否超过1个小时，超过则设置该皿目录为结束采集（已完成）
- 将结束采集时间更新到周期表 t_procedure 的结束采集时间中（未完成）
'''

def process_dish(path, dish_info):
    '''
    处理一个皿目录方法
        @param path: 采集目录完整路径
        @param dish_info: DishConfig配置信息对象
        @returns state: 皿结束采集标志 True - 已结束采集；False - 未结束采集
    '''
    from functools import partial
    dish_path = path + f'DISH{dish_info.index}' + os.path.sep # 皿目录完整路径
    logger.debug(f'处理皿目录: {dish_path}')
    if not dish_info.lastSerie:
        last_op = '0' * 7
    else:
        
        last_op = TimeSeries()[serie_to_minute(dish_info.lastSerie)//15+1]
    logger.debug(f'最后处理的时间序列: {last_op}')
    # 已经处理过的时间序列列表
    processed = TimeSeries().range(last_op)
    logger.debug(f'已经处理的时间序列: {processed}')
    # 以下两行代码使用偏函数从当前目录中得到所有合法且未处理的时间序列子目录
    f = partial(dir_filter, processed=processed, base=dish_path)
    pattern = re.compile(r'^[0-9]{7}$')
    todo = list(sorted(filter(lambda x: pattern.match(x) != None, os.listdir(dish_path))))

    logger.debug(f'未处理的时间序列: {todo}')

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
    '''
    datetime的timedelta有一个大坑，当now小于end_time时，即end_time还在现在时间之后的情况下，居然返回的是
    如 `-1 day, 23:49:08.318271` 这样的值，而不是 `0 day, - xxx` 这样的值。导致下面的or判断生效产生了一个
    严重bug。加上对days的非负判断后程序正常。
    
    以此注释记录此处问题及前因后果。
    '''
    if interval.days > 0 or (interval.days == 0 and interval.seconds > conf['ACTIVE_TIMEOUT']):
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