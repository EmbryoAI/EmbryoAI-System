#!/bin/env python
# -*- coding: utf8 -*-

from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout, Activation
from keras.losses import categorical_crossentropy
from keras import Sequential
from keras.optimizers import Adam

def init_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3,3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(64, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(128, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(256, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    model.add(Conv2D(512, (3,3)))
    model.add(Activation('relu'))
    model.add(MaxPool2D())
    # model.add(Conv2D(256, (3,3)))
    # model.add(Activation('relu'))
    # model.add(MaxPool2D())
    # model.add(Conv2D(128, (3,3)))
    # model.add(Activation('relu'))
    # model.add(MaxPool2D())
    # model.add(Conv2D(512, (3,3)))
    # model.add(Activation('relu'))
    # model.add(MaxPool2D())
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(14))
    model.add(Activation('softmax'))
    return model
