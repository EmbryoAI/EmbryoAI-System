# -*- coding: utf8 -*-

from keras.applications import InceptionV3, Xception, VGG16, VGG19, \
    ResNet50, InceptionResNetV2, MobileNet, MobileNetV2, DenseNet169, \
    DenseNet121, DenseNet201

'''
ImageNet预训练模型的帮助类，包括所有目前keras支持的ImageNet模型。
InceptionV3, Xception, VGG16, VGG19, 
ResNet50, InceptionResNetV2, MobileNet, MobileNetV2, DenseNet169, 
DenseNet121, DenseNet201
'''
class ImageNetModel():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if not hasattr(self, 'weights'):
            self.weights = None # 模型中参数初始化值，默认随机
        if not hasattr(self, 'include_top'):
            self.include_top = True # 是否包括输入层，默认包含
        if not hasattr(self, 'classes'):
            self.classes = 14 # 分类数量，0-13，共14类
        if not hasattr(self, 'input_shape'):
            self.input_shape = None # 输入图像shape
        if not hasattr(self, 'pooling'):
            self.pooling = None # 最后池化方式，默认无池化
    def getModel(self, model_type='InceptionV3'):
        '''
        获取ImageNet预训练模型的keras model对象
            @param: model_type 模型名称，默认InceptionV3
            @returns: keras model
        '''
        import sys
        mod = sys.modules[__name__]
        if hasattr(mod, model_type):
            func = getattr(mod, model_type)
            return func(include_top=self.include_top, weights=self.weights, 
                input_shape=self.input_shape, pooling=self.pooling, classes=self.classes)
        else:
            raise ValueError(f'ImageNet模型中没有找到 {model_type}')