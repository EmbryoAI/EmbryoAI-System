# -*- coding: utf8 -*-

from imageio import imread
from skimage.transform import resize
import numpy as np
import os

'''
将图像dataset目录下的文件读取到内存中进行学习，此方式适合数据量较小的情况，在数据量大的情况下，必须使用generator
'''
def preprocess_image(img):
    return (img/255-0.5)*2.0

def postprocess_image(img):
    return (img/2+0.5)*255

def read_dataset(data_path, size, classes=14):
    X_ = []
    y_ = []
    for i in range(classes):
        img_path = data_path + os.path.sep + str(i) + os.path.sep
        for img_file in filter(lambda x: x.endswith('.jpg'), os.listdir(img_path)):
            img = imread(img_path+img_file)
            img = resize(img, size)
            X_.append(img[...,np.newaxis])
            y_.append(i)
    X = np.array(X_)
    y = np.array(y_)
    print(f'Read dataset images into numpy array @ {X.shape}')
    print(f'Read dataset classes into numpy array @ {y.shape}')
    return X, y