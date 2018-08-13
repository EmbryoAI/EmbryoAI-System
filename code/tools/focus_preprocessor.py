#!/bin/env python
# -*- coding: utf8 -*-

from task.ini_parser import EmbryoIniParser
from task.TimeSeries import TimeSeries
from task.dish_config import DishConfig
from cv.ImageSharpnessTool import ImageSharpnessTool
from argparse import ArgumentParser
import os
import cv2
import numpy as np

def process_cycle(path):
    """
    处理图像采集目录方法
        @param path: 图像采集目录，按照采集设备的设定，该目录为一个14位数字的日期字符串，格式如YYYYMMDDHHmmss
    """
    dish_ini = EmbryoIniParser(path + 'DishInfo.ini') # 采集设备生成的INI配置文件
    print(f'正在处理采集图像文件夹 {path}')
    cycle_json = {}
    # print(dish_ini['Timelapse']['StartTime'])
    for i in range(1, 10):
        if f'Dish{i}Info' in dish_ini:
            cycle_json[i] = False
    for dish_index in cycle_json:
        dish_conf = DishConfig()
        dish_conf.dishSetup(dish_index, dish_ini[f'Dish{dish_index}Info'], int(dish_ini['Timelapse']['WellCount']))
        process_dish(path, dish_conf)

def process_dish(path, dish_info):
    '''
    处理一个皿目录方法
        @param path: 采集目录完整路径
        @param dish_info: DishConfig配置信息对象
    '''
    from functools import partial
    dish_path = path + f'DISH{dish_info.index}' + os.path.sep 
    print(f'processing dish {dish_path}')
    last_op = '0' * 7
    processed = TimeSeries().range(last_op)
    # 以下两行代码使用偏函数从当前目录中得到所有合法且未处理的时间序列子目录
    f = partial(dir_filter, processed=processed, base=dish_path)
    todo = list(sorted(filter(f, os.listdir(dish_path))))

    for serie in todo:
        # 交给process_serie_dir模块对时间序列目录进行处理
        process_serie(dish_path, serie, dish_info)

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

def process_serie(path, serie, dish_info):
    '''
    时间序列目录处理方法
        @param path: 皿目录完整路径
        @param serie: 时间序列字符串
        @dish_info: 皿配置信息 DishConfig对象
        @returns serie: 处理完的时间序列字符串
    '''
    serie_path = path + serie + os.path.sep # 时间序列目录完整路径
    wells = dish_info.wells # 皿中所有的孔信息
    for c in wells:
        print(f'处理 序列 {serie} 孔 {wells[c].index}')
        # 某个孔所有图像的完整路径列表
        well_image_files = [f'{serie_path}{i:05d}.jpg' for i in range(wells[c].fileStart, wells[c].fileEnd)]
        # 获得该孔的最清晰图像
        try :
            sharpest = find_sharpest(well_image_files)
            print(f'返回的最清晰图像路径 {sharpest}')
        except:
            sharpest = None
        if not sharpest:
            # 没有找到清晰图像，没有找到胚胎，使用序号中间的图像作为最清晰图，缩略图使用默认找不到胚胎的图像代替
            pass
        else:
            # 找到清晰图像
            img = read_img_grayscale(sharpest)
            # 定位胚胎位置
            left, top, right, bottom = find_embryo(img, cas)
            img_focus = img[top:bottom, left:right]
            focus_path = path + 'focus' + os.path.sep
            if not os.path.exists(focus_path):
                os.makedirs(focus_path)
            focus_file = f'{focus_path}Dish{dish_info.index:02d}_{wells[c].index:02d}_{serie}.jpg'
            # 保存缩略图
            cv2.imwrite(focus_file, img_focus, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

def find_sharpest(files):
    '''
    查找最清晰图像方法
        @param files: 一个孔的所有图像文件完整路径列表
        @returns filename: 最清晰图像文件完整路径，找不到返回None
    '''

    # 优先使用ImageSharpnessTool工具类查找最清晰图像，性能考虑
    all_sharpness = []
    for f in files:
        metrics = ImageSharpnessTool(read_img_grayscale(f), mode='gray')
        all_sharpness.append(metrics.sharpness_lap())
    sharpness_array = np.array(all_sharpness)
    index = np.argmax(sharpness_array) # 清晰度最大的序号为最清晰图像
    # 验证最清晰图像是否能检测到胚胎
    img = read_img_grayscale(files[index])
    embryo_box = find_embryo(img, cas)
    if not embryo_box is None:
        # 能检测到胚胎，直接返回该文件
        return files[index]
    # 否则，采用算法向Z轴两端去寻找能够检测到胚胎的图像，并作为最清晰图像
    reach_lowest = reach_highest = False
    low_index = high_index = index
    while True:
        low_index -= 1 # 向低端移动
        if low_index >= 0:
            img = read_img_grayscale(files[low_index])
            embryo_box = find_embryo(img, cas)
            if not embryo_box is None:
                # 检测到胚胎则返回
                return files[low_index]
        else:
            reach_lowest = True
        high_index += 1 # 向高端移动
        if high_index < len(files):
            img = read_img_grayscale(files[high_index])
            embryo_box = find_embryo(img, cas)
            if not embryo_box is None:
                # 检测到胚胎则返回
                return files[high_index]
        else:
            reach_highest = True
        if reach_lowest and reach_highest:
            # 最终所有Z轴图像都扫描过后，仍未检测到胚胎，返回None
            print('未能找到胚胎')
            return None

def read_img_grayscale(image_file):
    '''
    使用灰度模式读取图像工具方法
        @param image_file: 图像文件名
    '''
    return cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)

def find_embryo(img, cascade, minSize=(400, 400), maxSize=(600, 600)):
    '''
    在一张图像中对胚胎进行目标检测
        @param img: 图像numpy数组
        @param minSize: 胚胎目标最小尺寸，2元组
        @param maxSize: 胚胎目标最大尺寸，2元组
        @returns embryo_box: 胚胎目标的左上角坐标left, top和右下角坐标right, bottom，4元组
    '''
    rects, _, confidences = cascade.detectMultiScale3(img, minSize=minSize, maxSize=maxSize, outputRejectLevels=True)
    if len(rects) < 1:
        # 没有找到胚胎目标
        return None
    if len(rects) > 1:
        zone = rects[np.argmax(np.array(confidences))]
    else:
        zone = rects[0]
    # 将detectMultiScale返回的目标坐标和宽高转换为左上角和右下角坐标，并返回
    embryo_box = find_suitable_box(zone, img.shape)
    return embryo_box

def find_suitable_box(rect, shape):
    '''
    将宽高转换为右下角坐标返回，并固定目标区域像素为600x600，处理一些异常情况
        @param rect: detectMultiScale得到的目标坐标和宽高参数，4元组
        @param shape: 原始图像的高和宽
        @returns 左上角坐标left, top和右下角坐标right, bottom，4元组
    '''
    x, y, w, h = rect
    centerx, centery = x+(w//2), y+(h//2)
    left = centerx - 299
    top = centery - 299
    right = left + 600
    bottom = top + 600
    if left < 0:
        left = 0
        right = 600
    if top < 0:
        top = 0
        bottom = 600
    if right > shape[1]:
        right = shape[1]
        left = right - 600
    if bottom > shape[0]:
        bottom = shape[0]
        top = bottom - 600
    return left, top, right, bottom

cas = None
if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--image', help='采集图像目录路径', required=True)
    parser.add_argument('-c', '--cascade', help='Cascade分类器文件路径', required=True)
    conf = parser.parse_args()
    cas = cv2.CascadeClassifier(conf.cascade)
    process_cycle(conf.image)
