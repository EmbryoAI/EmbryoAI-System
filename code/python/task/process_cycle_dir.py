# -*- coding: utf8 -*-

from task.ini_parser import EmbryoIniParser
from task.dish_config import DishConfig
from task.process_dish_dir import process_dish
import json
from app import app

logger = app.logger

def process_cycle(path):
    dish_ini = EmbryoIniParser(path + 'DishInfo.ini')
    logger.debug(f'正在处理活动采集图像文件夹 {path}')
    try:
        with open(path + 'process_state.json') as fn:
            cycle_json = json.loads(fn.read())
    except:
        cycle_json = {}
        for i in range(1, 10):
            if f'Dish{i}Info' in dish_ini:
                cycle_json[i] = False
    finished = True
    for dish_index in cycle_json:
        if cycle_json[dish_index]:
            continue
        logger.debug(f'未结束的采集任务，皿号: {dish_index}')
        dish_conf = DishConfig(dish_index, dish_ini[f'Dish{dish_index}Info'])
        checkpoint = process_dish(path, dish_conf)
        cycle_json[dish_index] = checkpoint
        finished = finished & checkpoint
    with open(path + 'process_state.json', 'w') as fn:
        fn.write(json.dumps(cycle_json))
    return finished