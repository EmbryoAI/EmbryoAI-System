# -*- coding: utf8 -*-

from task.TimeSeries import TimeSeries
import os


def process_dish(path):
    from functools import partial
    dish_path = path + f'DISH{dish_info.index}' + os.path.sep
    try:
        last_op = open(dish_path + '.last_op').read()
    except:
        last_op = '0' * 7
    processed = TimeSeries().range(last_op)
    f = partial(dir_filter, processed=processed, base=dish_path)
    todo = list(sorted(filter(f, os.listdir(dish_path))))
    for serie in todo:
        # pass
        last_op = process_serie(dish_path, serie)
    with open(dish_path + '.last_op', 'w') as fn:
        fn.write(last_op)
    return check_finish_state(path, last_op)

def check_finish_state(path, last_serie):
    import datetime as dt
    from task.ini_parser import ConfigParser
    
    return True


def dir_filter(path, processed, base):
    if not os.path.isdir(base + path):
        return False
    if path in processed:
        return False
    if path == 'focus':
        return False
    return True