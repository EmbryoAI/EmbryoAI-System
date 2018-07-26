#!/bin/env python
# -*- coding: utf8 -*-

from argparse import ArgumentParser
from sklearn.model_selection import train_test_split
from keras.models import load_model
from keras.utils import np_utils
from dataset import read_dataset

NB_CLASSES = 14

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--dataset', help='数据集目录', required=True)
    parser.add_argument('-m', '--model', help='ImageNet模型名称', required=True)
    parser.add_argument('-s', '--size', help='图像尺寸', default='100')
    parser.add_argument('-b', '--batch', help='BATCH_SIZE每批图像数量', default='128')
    conf = parser.parse_args()
    img_size = (int(conf.size), int(conf.size))
    BATCH_SIZE = int(conf.batch)
    X, y = read_dataset(conf.dataset, img_size) # 将数据集全部读取到内存中
    # 使用sklearn将数据分为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1978)
    # 将输出进行onehot编码
    y_train = np_utils.to_categorical(y_train, num_classes=NB_CLASSES)
    y_test = np_utils.to_categorical(y_test, num_classes=NB_CLASSES)

    model = load_model(conf.model)
    model.summary()
    test_loss, test_metrics = model.evaluate(X_test, y_test, batch_size=BATCH_SIZE, verbose=1)
    print(f'Test Loss: {test_loss}, test metrics: {test_metrics}')
    