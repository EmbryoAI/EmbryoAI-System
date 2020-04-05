# -*- coding: utf8 -*-
import cv2
import numpy as np


class ImageSharpnessTool(object):
    """图像清晰度度量值计算类，提供三种算法计算图像度量值，拉普拉斯、sobel和SMD
       计算性能：laplace > sobel > SMD
       适应性：SMD > laplace > sobel
       应优先采用laplace算法计算图像清晰度，
       特别是囊胚之前的图像，laplace算法体现了性能和准确性的最优效果。
       囊胚阶段可以辅助采用SMD算法进行计算。
       sobel算法应尽量避免使用"""

    def __init__(self, img, mode="BGR"):
        if not isinstance(img, np.ndarray):
            raise TypeError("参数不是一个numpy张量")
        if img.ndim < 2 or img.ndim > 3:
            raise TypeError("参数numpy张量不是一张图像")
        if img.ndim == 3 and img.shape[2] not in (3, 4):
            raise ValueError("图像参数数据错误，非RGB图像或RGBA图像")
        if img.ndim == 3:
            if mode == "BGR":
                self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                self.img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        elif img.ndim == 4:
            if mode == "BGRA":
                self.img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            else:
                self.img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        else:
            self.img = img

    def sharpness_lap(self, kernel=3):
        """使用拉普拉斯算法求图像清晰度度量值"""
        img_lap = cv2.Laplacian(self.img, -1, ksize=kernel)
        return img_lap.mean()

    ### 单元测试完全通不过，放弃方差法
    """def sharpness_std(self):
        '''使用方差算法求图像清晰度度量值'''
        im = self.img.astype(np.int16)
        return self.img.var()"""

    def sharpness_sobel(self, kernel=3):
        """使用sobel算法求图像清晰度度量值"""
        img_sobel = cv2.Sobel(self.img, -1, 1, 1, ksize=kernel)
        return img_sobel.mean()

    def sharpness_smd(self):
        """使用SMD算法求图像清晰度度量值"""
        im = self.img.astype(np.float64)
        dx = np.abs(im[:-1, :] - im[1:, :]).sum()
        dy = np.abs(im[:, 1:] - im[:, :-1]).sum()
        return (dx + dy) / im.size


# 以下为单元测试

import unittest


class image_sharp_test(unittest.TestCase):
    def test(self):
        from TimeSeries import TimeSeries
        import os

        base_path = "/Users/wangying/git/repos/EmbryoAI-System/models/demo0/20170624151700/DISH1/"
        ts = TimeSeries()
        while True:
            next_frame = ts.next()
            frame_path = base_path + next_frame
            if next_frame in ("0184500", "4094500", "4103000", "4163000"):
                continue
            if not os.path.exists(frame_path):
                break
            sharp1 = ImageSharpnessTool(
                cv2.imread(frame_path + os.path.sep + "00001.jpg")
            )
            sharp6 = ImageSharpnessTool(
                cv2.imread(frame_path + os.path.sep + "00006.jpg")
            )
            sharp11 = ImageSharpnessTool(
                cv2.imread(frame_path + os.path.sep + "00011.jpg")
            )
            self.assertTrue(sharp1.sharpness_lap() < sharp6.sharpness_lap())
            self.assertTrue(sharp6.sharpness_lap() > sharp11.sharpness_lap())
            # self.assertTrue(sharp1.sharpness_sobel()<sharp6.sharpness_sobel())
            # self.assertTrue(sharp6.sharpness_sobel()>sharp11.sharpness_sobel())
            # self.assertTrue(sharp1.sharpness_std()<sharp6.sharpness_std())
            # self.assertTrue(sharp6.sharpness_std()>sharp11.sharpness_std())
            # self.assertTrue(sharp1.sharpness_smd()<sharp6.sharpness_smd())
            # self.assertTrue(sharp6.sharpness_smd()>sharp11.sharpness_smd())
            print(next_frame)


if __name__ == "__main__":
    unittest.main()
