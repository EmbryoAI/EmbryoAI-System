#!/bin/env python
# -*- coding: utf8 -*-

import os
import shutil
from argparse import ArgumentParser
import numpy as np

if __name__=='__main___':
    parser = ArgumentParser()
    parser.add_argument('-a', '--annotations', help='标注文件目录', required=True)
    parser.add_argument('-i', '--images', help='图像文件目录', required=True)
    parser.add_argument('-o', '--output', help='输出目录', required=True)
    args = parser.parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    for anno in filter(lambda x: x.endswith('.txt'), os.listdir(args.annotations)):
        img_array = np.genfromtxt(args.annotations + os.path.sep + anno)
        for i in range(len(img_array)):
            img_file = img_array[i][0]
            img_tag = img_array[i][1]
            output_tag = args.output + os.path.sep + img_tag
            if not os.path.exists(output_tag):
                os.makedirs(output_tag)
            img_src = args.images + os.path.sep + img_file
            img_dst = output_tag + os.path.sep + img_file
            shutil.move(img_src, img_dst)

