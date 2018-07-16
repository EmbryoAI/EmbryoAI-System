# -*- coding: utf8 -*-

from task.TimeSeries import TimeSeries
import os
from app import conf
from task.process_serie_dir import process_serie


def process_dish(path, dish_info):
    from functools import partial
    dish_path = path + f'DISH{dish_info.index}' + os.path.sep
    try:
        last_op = open(dish_path + conf['LAST_SERIE_FILENAME']).read()
    except:
        last_op = '0' * 7
    processed = TimeSeries().range(last_op)
    f = partial(dir_filter, processed=processed, base=dish_path)
    todo = list(sorted(filter(f, os.listdir(dish_path))))
    for serie in todo:
        # pass
        last_op = process_serie(dish_path, serie, dish_info)
        with open(dish_path + conf['LAST_SERIE_FILENAME'], 'w') as fn:
            fn.write(last_op)
    return check_finish_state(path, last_op)

def check_finish_state(path, last_serie):
    import datetime as dt
    from task.ini_parser import EmbryoIniParser
    ini_conf = EmbryoIniParser(path+'DishInfo.ini')
    start_ = ini_conf['Timelapse']['StartTime']
    start_time = dt.datetime.strptime(start_, '%Y%m%d%H%M%S')
    now = dt.datetime.now()
    interval = now - start_time
    if interval.days > 0 or interval.seconds > conf['ACTIVE_TIMEOUT']:
        return True
    return False


def dir_filter(path, processed, base):
    if not os.path.isdir(base + path):
        return False
    if path in processed:
        return False
    if path == 'focus':
        return False
    return True