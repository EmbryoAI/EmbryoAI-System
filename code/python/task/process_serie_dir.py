# -*- coding: utf8 -*-

import os, json
import cv2
import numpy as np
from cv.ImageSharpnessTool import ImageSharpnessTool
from cv.embryo_detector import find_embryo
from app import app
from task.dish_config import SerieInfo
from cv.embryo_common import outer_edge, cell_edge
from skimage.transform import resize
from common import getdefault

logger = app.logger # 日志

'''
### 时间序列目录处理模块，时间序列目录中，图像以5位数字字符串为名称存储，每个孔会占用Z轴层数个文件进行采集
#### 处理需要完成的工作包括：
- 获取每个孔的最清晰图片，并将完整路径写入JSON文件（已完成）
- 获取每个孔的略缩图，并将完整路径写入JSON文件（已完成）
- 获取每个孔的胚胎阶段（里程碑）分类，并将分类写入JSON文件（未完成）
- 更新数据库里程碑表 t_milestone 的数据（未完成）
- 更新最后处理时间序列的里程碑标志（未完成）
'''

stage_labels = ['未分裂', '1PN', '8C', '>=8C', '囊胚', '扩张囊胚', 
                '2PN', '3PN', '2C', '3C', '4C',
                '5C', '6C', '7C']

def process_serie(path, serie, dish_info):
    '''
    时间序列目录处理方法
        @param path: 皿目录完整路径
        @param serie: 时间序列字符串
        @dish_info: 皿配置信息 DishConfig对象
        @returns serie: 处理完的时间序列字符串
    '''
    from app import conf, model
    serie_path = path + serie + os.path.sep # 时间序列目录完整路径
    wells = dish_info.wells # 皿中所有的孔信息
    for c in wells:
        logger.debug(f'处理 序列 {serie} 孔 {wells[c].index}')
        # 某个孔所有图像的完整路径列表
        well_image_files = [f'{serie_path}{i:05d}.jpg' for i in range(wells[c].fileStart, wells[c].fileEnd)]
        # 获得该孔的最清晰图像
        try :
            sharpest = find_sharpest(well_image_files)
            logger.debug(f'返回的最清晰图像路径 {sharpest}')
        except:
            sharpest = None
        serie_info = SerieInfo()
        serie_info.serieSetup(wells[c], serie)
        if sharpest:
            # 找到清晰图像
            img = read_img_grayscale(sharpest)
            # 定位胚胎位置
            left, top, right, bottom = find_embryo(img)
            img_focus = img[top:bottom, left:right]
            img_out = cv2.resize(img_focus, (200, 200), cv2.INTER_NEAREST)
            img_size = getdefault(conf, 'EMBRYO_PREDICT_SIZE', 200)

            # 下面使用keras的预训练模型，对胚胎图像阶段进行预测
            img_predict = resize(img_focus, (img_size, img_size))
            img_predict = img_predict[np.newaxis, ..., np.newaxis]
            prediction = model.predict_classes(img_predict)
            print(prediction, stage_labels[prediction[0]])
            # img_class = prediction[0].argmax()
            serie_info.stage = stage_labels[prediction[0]]
            # print(prediction, stage_labels[prediction])

            focus_path = path + conf['EMBRYO_FOCUS_DIRNAME'] + os.path.sep
            if not os.path.exists(focus_path):
                os.makedirs(focus_path)
            focus_file = f'{wells[c].index:02d}_{serie}_focus.jpg'
            # 保存缩略图
            cv2.imwrite(focus_path + focus_file, img_out, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            outer_cnt, outer_area, outer_diameter = outer_edge(img)
            if len(outer_cnt):
                serie_info.outerArea = outer_area
                serie_info.outerDiameter = outer_diameter
            cell_result = cell_edge(img)
            if len(cell_result) == 1:
                serie_info.innerArea = cell_result[0][1]
                serie_info.innerDiameter = cell_result[0][2]
            if len(cell_result) == 2:
                serie_info.innerArea = cell_result[0][1]
                serie_info.innerDiameter = cell_result[0][2]
                serie_info.expansionArea = cell_result[1][1]
            if serie_info.outerDiameter and serie_info.innerDiameter \
                    and serie_info.outerDiameter > serie_info.innerDiameter:
                serie_info.zonaThickness = (serie_info.outerDiameter - serie_info.innerDiameter) * 0.425
            serie_info.embryoFound = True
            relative = os.path.split(sharpest)[1]
            serie_info.sharp = relative
            serie_info.focus = f"{conf['EMBRYO_FOCUS_DIRNAME']+os.path.sep}{focus_file}"
            wells[c].lastEmbryoSerie = serie
        wells[c].addSerie(serie_info)
    return serie

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
    embryo_box = find_embryo(img)
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
            embryo_box = find_embryo(img)
            if not embryo_box is None:
                # 检测到胚胎则返回
                return files[low_index]
        else:
            reach_lowest = True
        high_index += 1 # 向高端移动
        if high_index < len(files):
            img = read_img_grayscale(files[high_index])
            embryo_box = find_embryo(img)
            if not embryo_box is None:
                # 检测到胚胎则返回
                return files[high_index]
        else:
            reach_highest = True
        if reach_lowest and reach_highest:
            # 最终所有Z轴图像都扫描过后，仍未检测到胚胎，返回None
            return None

def read_img_grayscale(image_file):
    '''
    使用灰度模式读取图像工具方法
        @param image_file: 图像文件名
    '''
    return cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)