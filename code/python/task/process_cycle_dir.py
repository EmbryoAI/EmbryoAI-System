# -*- coding: utf8 -*-

import json
import os

from task.ini_parser import EmbryoIniParser
from task.dish_config import DishConfig
from task.process_dish_dir import process_dish
from app import conf
from common import nested_dict

import logUtils as logger # 日志

'''
### 处理某个采集目录的模块
#### 处理需要完成的工作包括：
- 读取采集设备生成的DishInfo.ini文件，并按照配置生成皿对象和孔对象（已完成）
- 从配置CYCLE_PROCESS_FILENAME设置的JSON文件中获取所有皿的处理状态，已处理完成的皿将被忽略（已完成）
- 所有的皿都处理完成后，返回True给调用者，用于设置整个采集目录的完成状态（已完成）
- 将进入某个有效（avail为1）的皿进行的处理交给process_dish_dir模块（已完成）
'''

def process_cycle(path):
    """
    处理图像采集目录方法
        @param path: 图像采集目录，按照采集设备的设定，该目录为一个14位数字的日期字符串，格式如YYYYMMDDHHmmss
        @returns finished: True - 全部皿处理完成；False - 该采集目录未完成
    """
    dish_ini = EmbryoIniParser(path + 'DishInfo.ini') # 采集设备生成的INI配置文件
    dish_count = int(dish_ini['Timelapse']['DishCount'])
    well_count = int(dish_ini['Timelapse']['WellCount'])
    logger.debug(f'正在处理活动采集图像文件夹 {path}')
    try:
        with open(path + conf['CYCLE_PROCESS_FILENAME']) as fn:
            # 如果JSON文件存在，读取皿目录的处理状态，True已完成，False未完成
            cycle_json = json.load(fn) 
    except:
        # JSON文件不存在，设置所有有效的皿目录的状态为False
        cycle_json = {}
        for i in range(1, dish_count+1):
            if f'Dish{i}Info' in dish_ini:
                cycle_json[i] = False
    finished = True
    for dish_index in cycle_json:
        if cycle_json[dish_index]:
            continue
        logger.debug(f'未结束的采集任务，皿号: {dish_index}')
        # 如果皿目录未结束，先读取皿目录下面的dish_state.json文件，如果文件不存在，则生成一个空的state JSON
        dish_path = path + f'DISH{dish_index}' + os.path.sep
        try:
            with open(dish_path+conf['DISH_STATE_FILENAME']) as fn:
                jstr = json.load(fn)
                dish_conf = DishConfig(jstr)
        except:        
            incubator_name = dish_ini['IncubatorInfo']['IncubatorName']
            dish_conf = DishConfig()
            dish_conf.dishSetup(dish_index, dish_ini[f'Dish{dish_index}Info'], well_count, incubator_name)
        checkpoint = process_dish(path, dish_conf) # 每个皿的目录为DISH+皿编号
        dish_conf.finished = checkpoint
        with open(dish_path+conf['DISH_STATE_FILENAME'], 'w') as fn:
            fn.write(json.dumps(nested_dict(dish_conf)))

        # if checkpoint :
        #     is_upload = upload_dish(path, dish_conf)

        # 设置皿目录是否结束采集标志，该标志checkpoint由process_dish方法返回
        cycle_json[dish_index] = checkpoint
        finished = finished and checkpoint # 所有皿目录处理完成标志

        # 将处理完成的皿目录下的图像上传到minio


    # 写入JSON文件
    with open(path + conf['CYCLE_PROCESS_FILENAME'], 'w') as fn:
        fn.write(json.dumps(cycle_json))
    return finished # 返回所有皿目录处理完成标志
