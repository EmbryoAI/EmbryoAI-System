# -*- coding: utf8 -*-

from app import conf
from task.process_cycle_dir import process_cycle
import json
import os
from app import app

logger = app.logger
finished_json = conf['FINISHED_JSON_FILENAME']

def run():
    cap_dir = conf['EMBRYOAI_IMAGE_ROOT']
    if not cap_dir.endswith(os.path.sep):
        cap_dir += os.path.sep
    logger.debug(f'进入定时图像处理任务,采集图像目录为: {cap_dir}')
    active_dirs, finished_dirs = find_active_dirs(cap_dir)
    logger.debug(f'需要处理的目录: {active_dirs}')
    for adir in active_dirs:
        cycle_dir = cap_dir + adir + os.path.sep
        state = process_cycle(cycle_dir)
        if state:
            finished_dirs.append(adir)
    with open(cap_dir + finished_json, 'w') as fn:
        fn.write(json.dumps(finished_dirs))
    logger.debug('结束定时任务')

def find_active_dirs(path):
    json_file = path + finished_json
    logger.debug(f'查找活动的目录: {path}, json文件为 {json_file}')
    try:
        with open(json_file) as fn:
            finished = json.loads(fn.read())
    except:
        logger.debug('json文件不存在，创建中')
        with open(json_file, 'w') as fn:
            fn.write('[]')
        finished = []
    logger.debug(f'已完成采集的目录: {finished}')
    # if finished:
    #     all_subs = find_last_10_days(path)
    # else:
    all_subs = list(filter(lambda x: os.path.isdir(path + x), os.listdir(path)))
    return list(filter(lambda x: x not in finished, all_subs)), finished

def find_last_10_days(path):
    import datetime as dt
    import numpy as np
    from functools import partial, reduce
    import glob2
    logger.debug('查找最近10天开始的采集目录')
    now = dt.datetime.now()
    last_10_days = np.arange(now-dt.timedelta(9), now+dt.timedelta(1), dt.timedelta(1), dtype=dt.date)
    to_date_str = np.vectorize(partial(dt.datetime.strftime, format='%Y%m%d'))
    dir_prefix = to_date_str(last_10_days).tolist()
    dir_list = reduce(list.__add__, [glob2.glob(d+'*') for d in dir_prefix])
    return list(filter(lambda x: os.path.isdir(path + x), dir_list))
