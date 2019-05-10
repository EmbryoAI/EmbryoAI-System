# -*- coding: utf8 -*-

from app import conf
from task.process_cycle_dir import process_cycle
import json
import os
import logUtils as logger

'''
### 定时任务模块，flask-scheduler通过调用run方法监控图像采集任务。
#### 定时任务需要完成的工作包括：
- 进入未完成采集的图像采集目录，并对最新采集的皿、序列进行处理，所有已完成采集的图像目录列表存入
  EMBRYOAI_IMAGE_ROOT配置所指定的JSON文件当中（已完成）
- 如果有从未处理过的皿、序列目录，需要添加一个新的周期到周期表 t_procedure，提供进行新建病历的操作（未完成）
- 然后进入到每个采集目录，交给process_cycle_dir模块进行处理（已完成）
'''

finished_json = conf['FINISHED_JSON_FILENAME'] # 已完成的采集目录列表JSON文件名称

def run():
    ''' 定时任务入口方法 '''
    # 读取配置的EMBRYOAI_IMAGE_ROOT，此为采集图像的根目录，开发测试阶段在app中设置为../captures。
    # 避免开发人员的操作系统的不一致造成配置的无法使用
    cap_dir = conf['EMBRYOAI_IMAGE_ROOT']
    if not cap_dir.endswith(os.path.sep):
        cap_dir += os.path.sep # 如结束符号不是/，加上/
    logger.debug(f'进入定时图像处理任务,采集图像目录为: {cap_dir}')

    # 获取未完成采集的目录列表
    active_dirs, finished_dirs = find_active_dirs(cap_dir)
    logger.debug(f'需要处理的目录: {active_dirs}')


    for adir in active_dirs:
        cycle_dir = cap_dir + adir + os.path.sep # 未完成采集目录的全路径
        # 交给process_cycle_dir模块进行处理采集目录，返回True或False，代表该采集目录采集结束标志
        state = process_cycle(cycle_dir)  
        # 如果state为True，而且原本的目录就为False存在json中，更新相应的值，而不是append
        if state and {adir: False} in finished_dirs:
            findex = finished_dirs.index({adir: False})
            finished_dirs[findex][adir] = True
        # 否则如果目录及状态不存在在json列表中，append
        elif {adir: state} not in finished_dirs:
            finished_dirs.append({adir: state}) # 采集结束则将该目录添加到结束目录列表中
    # 保存JSON文件
    with open(cap_dir + finished_json, 'w') as fn:
        json.dump(finished_dirs, fn)
    
    logger.debug('结束定时任务')

def find_active_dirs(path):
    '''
    获取path目录下所有未完成的采集目录列表
        @param path 目标目录完整路径
    '''

    json_file = path + finished_json # 存储结束采集目录列表的JSON文件
    try:
        with open(json_file) as fn:
            finished = json.load(fn) # 文件存在则读取文件的内容
    except:
        # 文件不存在则创建一个JSON文件，并写入一个空列表
        with open(json_file, 'w') as fn:
            fn.write('[]')
        finished = []
    logger.debug(f'已完成采集的目录: {finished}')
    # 仅读取10天以内开始采集的目录，为了导入历史采集目录，这里屏蔽了这几行代码
    # if finished:
    #     all_subs = find_last_10_days(path)
    # else:

    # 过滤掉所有非子目录的内容
    all_subs = list(filter(lambda x: os.path.isdir(path + x) and x.endswith('00'), os.listdir(path)))
    # 返回一个包括未完成采集及已完成采集目录列表的元组
    return list(filter(lambda x: {x: True} not in finished, all_subs)), finished

def find_last_10_days(path):
    '''
    在path目录下查找所有10天以内开始采集的目录并返回列表
        @param path 目标目录完整路径
    '''
    import datetime as dt
    import numpy as np
    from functools import partial, reduce
    import glob2
    logger.debug('查找最近10天开始的采集目录')
    # 当前系统时间now和一个10天日期的numpy数组last_10_days
    now = dt.datetime.now()
    last_10_days = np.arange(now-dt.timedelta(9), now+dt.timedelta(1), dt.timedelta(1), dtype=dt.date)
    # 下面两行代码创建一个numpy向量化偏函数用于将时间转化为YYYYMMDD格式
    to_date_str = np.vectorize(partial(dt.datetime.strftime, format='%Y%m%d'))
    dir_prefix = to_date_str(last_10_days).tolist()
    # 用通配符找到的符合日期的目录列表合并成一个dir_list
    dir_list = reduce(list.__add__, [glob2.glob(d+'*') for d in dir_prefix])
    # 过滤掉非子目录的内容并返回
    return list(filter(lambda x: os.path.isdir(path + x), dir_list))
