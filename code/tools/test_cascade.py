#!/bin/env python
# -*- coding: utf8 -*-

from argparse import ArgumentParser
import cv2
import os
import sys

def embryo_cascade(cascade, img, minSize=(400, 400), maxSize=None):
    if not cascade:
        raise ValueError(f'cascade分类器文件错误')
    rects = cascade.detectMultiScale(img, minSize=minSize, maxSize=maxSize)
    if len(rects):
        return 1
    return 0

if __name__=='__main__':
    import numpy as np
    parser = ArgumentParser()
    parser.add_argument('-i', '--image', help='输入图像目录路径，里面的所有jpg文件都会被处理', required=True)
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-c', '--cascade', help='cascade分类器文件路径', required=True)
    conf = parser.parse_args()
    cv2.Laplacian(np.zeros((100,100)), -1)
    cascade = cv2.CascadeClassifier(conf.cascade)
    count = 0
    all_images = []
    for root, dirnames, filenames in os.walk(conf.image):
        all_images += [os.path.join(root, f) for f in filenames if f.endswith('.jpg')]
    left = total = len(all_images)
    for f in all_images:
        sys.stdout.write(f'共 {total} 个文件，剩余 {left-1} 个文件 ...... {(total-left+1)/total*100:.2f}%\r')
        count+=embryo_cascade(cascade, cv2.imread(f, cv2.IMREAD_GRAYSCALE))
        left -= 1
        if not left:
            print()
            break
        sys.stdout.write(' '*80+'\r')
    print(f'总共定位到 {count} 个胚胎图像')