# -*- coding: utf8 -*-

from imageio import imread
from skimage.transform import resize
import numpy as np
import os

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
            X_.append(img)
            y_.append(i)
    X = np.array(X_)
    y = np.array(y_)
    print(f'Read dataset images into numpy array @ {X.shape}')
    print(f'Read dataset classes into numpy array @ {y.shape}')
    return X, y