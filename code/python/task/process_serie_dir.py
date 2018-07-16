# -*- coding: utf8 -*-

import os, json
import cv2
import numpy as np
from cv.ImageSharpnessTool import ImageSharpnessTool
from cv.embryo_detector import find_embryo
from app import app

logger = app.logger

def process_serie(path, serie, dish_info):
    from app import app_root, conf
    serie_path = path + serie + os.path.sep
    wells = dish_info.wells
    well_info = {}
    for c in wells:
        logger.debug(f'处理 序列 {serie} 孔 {c.index}')
        well_image_files = [f'{serie_path}{i:05d}.jpg' for i in range(c.fileStart, c.fileEnd)]
        sharpest = find_sharpest(well_image_files)
        logger.debug(f'返回的最清晰图像路径 {sharpest}')
        if not sharpest:
            # 没有找到清晰图像，没有找到胚胎，使用序号中间的图像作为最清晰图，缩略图使用默认找不到胚胎的图像代替
            logger.info(f'序列 {serie} 孔 {c.index} 中找不到到胚胎，使用中间序号图像作为最清晰图，缩略图使用默认找不到胚胎图像')
            sharpest = f'{serie_path}{(c.fileStart+c.fileEnd)//2:05d}.jpg'
            focus_file = app_root + 'cv' + os.path.sep + 'embryo_not_found.jpg'
        else:
            img = read_img_grayscale(sharpest)
            left, top, right, bottom = find_embryo(img)
            img_focus = img[top:bottom, left:right]
            focus_path = serie_path + 'focus' + os.path.sep
            if not os.path.exists(focus_path):
                os.makedirs(focus_path)
            focus_file = f'{focus_path}{c.index}_focus.jpg'
            print(img_focus.shape)
            cv2.imwrite(focus_file, img_focus)
        file_info = {'sharp': sharpest, 'focus': focus_file}
        well_info[c.index] = file_info
    with open(serie_path+conf['WELL_JSON_FILENAME'], 'w') as fn:
        fn.write(json.dumps(well_info))
    return serie

def find_sharpest(files):
    all_sharpness = []
    for f in files:
        metrics = ImageSharpnessTool(read_img_grayscale(f), mode='gray')
        all_sharpness.append(metrics.sharpness_lap())
    sharpness_array = np.array(all_sharpness)
    index = np.argmax(sharpness_array)
    img = read_img_grayscale(files[index])
    embryo_box = find_embryo(img)
    if not embryo_box is None:
        return files[index]
    reach_lowest = reach_highest = False
    low_index = high_index = index
    while True:
        low_index -= 1
        if low_index >= 0:
            img = read_img_grayscale(files[low_index])
            embryo_box = find_embryo(img)
            if not embryo_box is None:
                return files[low_index]
        else:
            reach_lowest = True
        high_index += 1
        if high_index < len(files):
            img = read_img_grayscale(files[high_index])
            embryo_box = find_embryo(img)
            if not embryo_box is None:
                return files[high_index]
        else:
            reach_highest = True
        if reach_lowest and reach_highest:
            return None

def read_img_grayscale(image_file):
    return cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)