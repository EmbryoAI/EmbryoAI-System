#!/bin/env python
# -*- coding: utf8 -*-

from argparse import ArgumentParser
import os
from imagenet_model import ImageNetModel
from dataset import read_dataset
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from train_model import init_model
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

NB_CLASSES = 14


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--dataset', help='数据集目录', required=True)
    parser.add_argument('-m', '--model', help='ImageNet模型名称', default='Xception')
    parser.add_argument('-o', '--output', help='输出模型及参数文件目录', required=True)
    parser.add_argument('-s', '--size', help='训练图像尺寸', default='100')
    parser.add_argument('-e', '--epochs', help='EPOCHS批次', default='20')
    parser.add_argument('-b', '--batch', help='BATCH_SIZE每批图像数量', default='128')
    parser.add_argument('-t', '--optimizer', help='梯度优化函数名称', default='Adam')
    conf = parser.parse_args()
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    tf_config.log_device_placement = True
    sess = tf.Session(config=tf_config)
    set_session(sess)
    img_size = (int(conf.size), int(conf.size))
    EPOCHS = int(conf.epochs)
    BATCH_SIZE = int(conf.batch)
    # X, y = read_dataset(conf.dataset, img_size)
    train_data = ImageDataGenerator(
        # rotation_range=180, 
        # horizontal_flip=True, 
        # vertical_flip=True, 
        rescale=1.0/255
        )
    val_data = ImageDataGenerator(rescale=1.0/255)
    test_data = ImageDataGenerator(rescale=1.0/255)
    train_gen = train_data.flow_from_directory(conf.dataset+os.path.sep+'train', 
        target_size=img_size, color_mode='grayscale', batch_size=BATCH_SIZE, seed=1978)
    val_gen = val_data.flow_from_directory(conf.dataset+os.path.sep+'validation', 
        target_size=img_size, color_mode='grayscale', batch_size=BATCH_SIZE)
    test_gen = test_data.flow_from_directory(conf.dataset+os.path.sep+'test', 
        target_size=img_size, color_mode='grayscale', batch_size=BATCH_SIZE)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1978)
    # y_train = np_utils.to_categorical(y_train, num_classes=NB_CLASSES)
    # y_test = np_utils.to_categorical(y_test, num_classes=NB_CLASSES)
    
    # model = ImageNetModel(weights=None, input_shape=(img_size[0], img_size[1], 1)).getModel(conf.model)
    if conf.model == 'custom':
        model = init_model((img_size[0], img_size[1], 1))
    else:
        model = ImageNetModel(weights=None, input_shape=(img_size[0], img_size[1], 1)).getModel(conf.model)
    model.compile(optimizer=conf.optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    # model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, verbose=1, validation_split=0.25)
    model.fit_generator(train_gen, epochs=EPOCHS, validation_data=val_gen, verbose=1)
    # model.evaluate(X_test, y_test, batch_size=BATCH_SIZE, verbose=1)
    test_loss, test_metrics = model.evaluate_generator(test_gen, verbose=1)
    print(f'Test Loss: {test_loss}, test metrics: {test_metrics}')
    if not os.path.exists(conf.output):
        os.makedirs(conf.output)
    model.save(f'{conf.output}{os.path.sep}{conf.model}.h5')