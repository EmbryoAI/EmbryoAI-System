#!/bin/env python
# -*- coding: utf8 -*-

import os
import shutil
from argparse import ArgumentParser
import numpy as np

'''
胚胎图像分类DNN学习预处理器
'''
if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-a', '--annotations', help='标注文件目录', required=True)
    parser.add_argument('-i', '--images', help='图像文件目录', required=True)
    parser.add_argument('-o', '--output', help='输出目录', required=True)
    parser.add_argument('-t', '--test', help='测试数据集比例', default='0.2')
    parser.add_argument('-v', '--validation', help='验证数据集比例', default='0.33')
    args = parser.parse_args()
    test_ratio = float(args.test)
    val_ratio = float(args.validation)
    # 设置一个幸运数字作为随记种子，方便后续重复性实验
    np.random.seed(19880520)
    # 如果输出目录不存在，创建它
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    # 读取所有的标注文件，按照一定验证数据集和测试数据集比例，将图像文件存放在不同的目录下，方便后续keras进行学习
    for anno in filter(lambda x: x.endswith('.txt'), os.listdir(args.annotations)):
        # 使用numpy将标注文件内容读出到一个array中
        img_array = np.genfromtxt(args.annotations + os.path.sep + anno, dtype=np.object)
        # 处理array中的每一行，根据不同的tag（0-13），将图像文件复制到相应的目录下
        for i in range(len(img_array)):
            test_flag = np.random.rand()
            val_flag = np.random.rand()
            if test_flag < test_ratio:
                output_path = args.output + os.path.sep + 'test'
            else:
                if val_flag < test_ratio:
                    output_path = args.output + os.path.sep + 'validation'
                else:
                    output_path = args.output + os.path.sep + 'train' 
            img_file = str(img_array[i][0], encoding='utf8')
            img_tag = f'{int(str(img_array[i][1], encoding="utf8")):02d}'
            output_tag = output_path + os.path.sep + img_tag
            if not os.path.exists(output_tag):
                os.makedirs(output_tag)
            img_src = args.images + os.path.sep + img_file
            img_dst = output_tag + os.path.sep + img_file
            shutil.copy(img_src, img_dst)

