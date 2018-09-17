#!/bin/env python
# -*- coding: utf8 -*-

from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout, Activation
from keras.losses import categorical_crossentropy
from keras import Sequential
from keras.optimizers import Adam

def init_model(input_shape):
    kernel = (2, 2)
    model = Sequential()
    model.add(Conv2D(32, kernel, input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(64, kernel))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(128, kernel))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(256, kernel))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(512, kernel))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    # model.add(Conv2D(1024, kernel))
    # model.add(Activation('relu'))
    # model.add(MaxPool2D())
    # model.add(Conv2D(2048, kernel))
    # model.add(Activation('relu'))
    # model.add(MaxPool2D())
    # model.add(Conv2D(4096, kernel))
    # model.add(Activation('relu'))
    # model.add(MaxPool2D())
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(14, activation='softmax'))
    return model
