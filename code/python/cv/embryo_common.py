# -*- coding: utf8 -*-

import numpy as np
import cv2

def to_BGR(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# 求胚胎外部轮廓
def outer_edge(img, thresh=3500, resol=3.75):
    from math import pi
    # 非邻近点平均值算法去噪
    img1 = cv2.fastNlMeansDenoising(img, 10, 4, 1)
    # 可适应性高斯算法求图像临界区
    img2 = cv2.adaptiveThreshold(img1, 5, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 3, 1)
    # 拉普拉斯算法求图像边缘
    img3 = cv2.Laplacian(img2, cv2.CV_64F, ksize=1).astype(np.uint8)
    # 求图像所有闭合轮廓
    _, cnt, hier = cv2.findContours(img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    area_array = np.array([cv2.contourArea(c) for c in cnt])
    max_area = area_array.max()/(resol*resol)
    if max_area > thresh:
        return cnt[np.argmax(area_array)], max_area, np.sqrt(max_area/pi)*2
    else:
        return None, None, None

# 求胚胎细胞轮廓
def cell_edge(img, thresh=2500, resol=3.75):
    from math import pi
    img1 = cv2.fastNlMeansDenoising(img, 10, 4, 5)
    img2 = cv2.adaptiveThreshold(img1, 5, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 1)
    img3 = cv2.Laplacian(img2, cv2.CV_64F, ksize=3).astype(np.uint8)
    _, cnt, hier = cv2.findContours(img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    area_array = np.array([cv2.contourArea(c)/(resol*resol) for c in cnt])
    cnt = np.array(cnt)
    avail_zone = cnt[area_array>thresh]
    avail_area = area_array[area_array>thresh]
    if len(avail_zone) == 2:
        return ((avail_zone[0], avail_area[0], np.sqrt(avail_area[0]/pi)*2),
                (avail_zone[1], avail_area[1], np.sqrt(avail_area[1]/pi)*2))
    elif len(avail_zone) == 1:
        return ((avail_zone[0], avail_area[0], np.sqrt(avail_area[0]/pi)*2),)
    else:
        return None, None, None

