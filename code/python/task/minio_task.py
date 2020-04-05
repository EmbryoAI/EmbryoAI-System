from app import conf
import json
import os
from task.dish_config import DishConfig
from app import app
from task.ini_parser import EmbryoIniParser
from task.upload_minio import upload_dish

"""
### 定时任务模块，flask-scheduler通过调用run方法监控图像采集任务。
#### 定时任务需要完成的工作包括：
- 进入未完成采集的图像采集目录，并对最新采集的皿、序列进行处理，所有已完成采集的图像目录列表存入
  EMBRYOAI_IMAGE_ROOT配置所指定的JSON文件当中（已完成）
- 如果有从未处理过的皿、序列目录，需要添加一个新的周期到周期表 t_procedure，提供进行新建病历的操作（未完成）
- 然后进入到每个采集目录，交给process_cycle_dir模块进行处理（已完成）
"""

import logUtils as logger  # 日志

finished_json = conf["FINISHED_JSON_FILENAME"]  # 已完成的采集目录列表JSON文件名称


def run():
    """ 定时任务入口方法 """
    # 读取配置的EMBRYOAI_IMAGE_ROOT，此为采集图像的根目录，开发测试阶段在app中设置为../captures。
    # 避免开发人员的操作系统的不一致造成配置的无法使用
    cap_dir = conf["EMBRYOAI_IMAGE_ROOT"]
    if not cap_dir.endswith(os.path.sep):
        cap_dir += os.path.sep  # 如结束符号不是/，加上/
    logger.debug(f"进入定时图像上传任务,采集图像目录为: {cap_dir}")

    finished = find_active_dirs(cap_dir)
    print(finished)
    logger.debug(f"需要上传的目录: {finished}")
    for adir in finished:
        print(adir)
        cycle_dir = cap_dir + adir + os.path.sep  # 未完成采集目录的全路径
        # 交给process_cycle_dir模块进行处理采集目录，返回True或False，代表该采集目录采集结束标志
        state = process_cycle(cycle_dir, adir)
    logger.debug("结束定时任务")


def find_active_dirs(path):
    """
    获取path目录下所有未完成的采集目录列表
        @param path 目标目录完整路径
    """

    json_file = path + finished_json  # 存储结束采集目录列表的JSON文件
    try:
        with open(json_file) as fn:
            finished = json.load(fn)  # 文件存在则读取文件的内容
    except:
        # 文件不存在则创建一个JSON文件，并写入一个空列表
        with open(json_file, "w") as fn:
            fn.write("[]")
        finished = []
    logger.debug(f"已完成采集的目录: {finished}")
    # 仅读取10天以内开始采集的目录，为了导入历史采集目录，这里屏蔽了这几行代码
    # if finished:
    #     all_subs = find_last_10_days(path)
    # else:

    # 过滤掉所有非子目录的内容
    all_subs = list(
        filter(lambda x: os.path.isdir(path + x) and x.endswith("00"), os.listdir(path))
    )
    # 返回一个包括未完成采集及已完成采集目录列表的元组
    return list(filter(lambda x: {x: True} in finished, all_subs))


def process_cycle(path, air):

    """
    处理图像采集目录方法
        @param path: 图像采集目录，按照采集设备的设定，该目录为一个14位数字的日期字符串，格式如YYYYMMDDHHmmss
        @returns finished: True - 全部皿处理完成；False - 该采集目录未完成
    """
    dish_ini = EmbryoIniParser(path + "DishInfo.ini")  # 采集设备生成的INI配置文件
    dish_count = int(dish_ini["Timelapse"]["DishCount"])
    well_count = int(dish_ini["Timelapse"]["WellCount"])
    logger.debug(f"正在处理活动采集图像文件夹 {path}")
    try:
        with open(path + conf["CYCLE_PROCESS_FILENAME"]) as fn:
            # 如果JSON文件存在，读取皿目录的处理状态，True已完成，False未完成
            cycle_json = json.load(fn)
    except:
        # JSON文件不存在，设置所有有效的皿目录的状态为False
        cycle_json = {}
        for i in range(1, dish_count + 1):
            if f"Dish{i}Info" in dish_ini:
                cycle_json[i] = False
    is_upload = True
    for dish_index in cycle_json:
        if cycle_json[dish_index]:
            logger.debug(f"未结束的采集任务，皿号: {dish_index}")
            # 如果皿目录未结束，先读取皿目录下面的dish_state.json文件，如果文件不存在，则生成一个空的state JSON
            dish_path = path + f"DISH{dish_index}" + os.path.sep
            print(dish_path)
            try:
                with open(dish_path + conf["DISH_STATE_FILENAME"]) as fn:
                    jstr = json.load(fn)
                    dish_conf = DishConfig(jstr)
            except:
                incubator_name = dish_ini["IncubatorInfo"]["IncubatorName"]
                dish_conf = DishConfig()
                dish_conf.dishSetup(
                    dish_index,
                    dish_ini[f"Dish{dish_index}Info"],
                    well_count,
                    incubator_name,
                )

            # 将处理完成的皿目录下的图像上传到minio
            is_upload = is_upload & upload_dish(path, dish_conf, air)
            print(is_upload)
    return is_upload  # 返回所有皿目录处理完成标志
