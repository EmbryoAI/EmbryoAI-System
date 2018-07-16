# -*- coding: utf8 -*-

import cv2
import os

'''
使用opencv cascade分类器对图像中胚胎进行目标检测的模块
'''

def find_embryo(img, minSize=(400, 400), maxSize=(600, 600)):
    '''
    在一张图像中对胚胎进行目标检测
        @param img: 图像numpy数组
        @param minSize: 胚胎目标最小尺寸，2元组
        @param maxSize: 胚胎目标最大尺寸，2元组
        @returns embryo_box: 胚胎目标的左上角坐标left, top和右下角坐标right, bottom，4元组
    '''
    from app import conf, app_root
    from common import getdefault, logger
    cascade_file = getdefault(conf, 'CASCADE_TEMPLATE', 'embryo_cascade.xml') # 配置的cascade分类器文件名
    cascade = cv2.CascadeClassifier(os.path.dirname(__file__) + os.path.sep + cascade_file)
    rects = cascade.detectMultiScale(img, minSize=minSize, maxSize=maxSize)
    if len(rects) < 1:
        # 没有找到胚胎目标
        return None
    if len(rects) > 1:
        # 找到多于一个胚胎目标，此情况表示有一定错误发生，目前暂未处理
        pass
    # 将detectMultiScale返回的目标坐标和宽高转换为左上角和右下角坐标，并返回
    embryo_box = find_suitable_box(rects[0], img.shape)
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