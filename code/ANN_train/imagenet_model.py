# -*- coding: utf8 -*-

from keras.applications import InceptionV3, Xception, VGG16, VGG19, \
    ResNet50, InceptionResNetV2, MobileNet, MobileNetV2, DenseNet169, \
    DenseNet121, DenseNet201

class ImageNetModel():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if not hasattr(self, 'weights'):
            self.weights = 'imagenet'
        if not hasattr(self, 'include_top'):
            self.include_top = True
        if not hasattr(self, 'classes'):
            self.classes = 14
        if not hasattr(self, 'input_shape'):
            self.input_shape = None
        if not hasattr(self, 'pooling'):
            self.pooling = None
    def getModel(self, model_type='InceptionV3'):
        import sys
        mod = sys.modules[__name__]
        if hasattr(mod, model_type):
            func = getattr(mod, model_type)
            return func(include_top=self.include_top, weights=self.weights, 
                input_shape=self.input_shape, pooling=self.pooling, classes=self.classes)
        else:
            raise ValueError(f'ImageNet模型中没有找到 {model_type}')