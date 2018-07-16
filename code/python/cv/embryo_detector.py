# -*- coding: utf8 -*-

import cv2
import os

def find_embryo(img, minSize=(400, 400), maxSize=(600, 600)):
    from app import conf, app_root
    from common import getdefault, logger
    cascade_file = getdefault(conf, 'CASCADE_TEMPLATE', 'embryo_cascade.xml')
    cascade = cv2.CascadeClassifier(os.path.dirname(__file__) + os.path.sep + cascade_file)
    rects = cascade.detectMultiScale(img, minSize=minSize, maxSize=maxSize)
    if len(rects) < 1:
        #logger().error('No embryos found in image.')
        return None
    if len(rects) > 1:
        pass
        #logger().warn('More than one embryos found in image.')
    embryo_box = find_suitable_box(rects[0], img.shape)
    return embryo_box

def find_suitable_box(rect, shape):
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