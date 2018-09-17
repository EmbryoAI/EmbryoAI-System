#!/bin/env python
# -*- coding: utf8 -*-

from keras.models import load_model
import numpy as np
from argparse import ArgumentParser
import os, shutil
import cv2

tags = [f'{i:02d}' for i in range(14)]

def classify_embryos(model, imgs, model_path, batch_size=32):
    # assert len(imgs.shape) == 4 and imgs.shape[1] == 200 and imgs.shape[2] == 200 and imgs.shape[3] == 1
    result_y = []
    y_ = model.predict(imgs, batch_size, verbose=1)
    for r in y_:
        if r.max()>0.9:
            result_y.append(r.argmax())
    return y_.argmax(axis=-1)

def form_input(path, img_files, img_size):
    array = []
    for f in img_files:
        img = cv2.imread(path + f, cv2.IMREAD_GRAYSCALE)/255.0
        img = cv2.resize(img, (img_size, img_size), cv2.INTER_NEAREST)[..., np.newaxis]
        array.append(img)
    return np.array(array)

def save_classify_imgs(y, src, files, dst):
    for i in range(len(y)):
        r = y[i]
        subdir = tags[r]
        if not os.path.exists(dst + subdir):
            os.makedirs(dst + subdir)
        # print(src+files[i], dst+subdir+os.path.sep+files[i])
        shutil.copy(src+files[i], dst+subdir+os.path.sep+files[i])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--images', help='需要预分类的图像目录', required=True)
    parser.add_argument('-m', '--model', help='keras模型文件路径', required=True)
    parser.add_argument('-o', '--output', help='输出图像目录', required=True)
    # parser.add_argument('-a', '--annotation', help='标注文本文件路径', required=True)
    parser.add_argument('-s', '--size', help='预分类图像尺寸', default=200)
    parser.add_argument('-b', '--batch', help='分批次图像数量', default=32)
    conf = parser.parse_args()
    conf.batch = int(conf.batch)
    conf.size = int(conf.size)
    model = load_model(conf.model)
    all_imgs = os.listdir(conf.images)
    end = 0
    for i in range(conf.batch, len(all_imgs), conf.batch):
        batch_imgs = form_input(conf.images, all_imgs[end: end+conf.batch], conf.size)
        end = i
        y = classify_embryos(model, batch_imgs, conf.model, len(batch_imgs))
        print(y)
        save_classify_imgs(y, conf.images, all_imgs[end: end+conf.batch], conf.output)

    batch_imgs = form_input(conf.images, all_imgs[end:], conf.size)
    y = classify_embryos(model, batch_imgs, conf.model, len(batch_imgs))
    print(y)
