from argparse import ArgumentParser
import cv2
import numpy as np
import os

TAG_MESSAGE = """标签及按键说明：
0 = 无分裂胚胎；
1 = 1PN胚胎；
2 = 2PN胚胎；
3 = >=3PN胚胎；
4 = 2C胚胎；
5 = 3C胚胎；
6 = 4C胚胎；
7 = 5C胚胎；
8 = 6C胚胎；
9 = 7C胚胎；
a/A = 8C胚胎；
b/B = >=8C胚胎
c/C = 囊胚；
d/D = 扩张囊胚；
q/Q/[ESC] = 退出；
n/N = 确认并显示下一张图像；
p/P = 上一张图像；"""

TAG_KEYS = [chr(_) for _ in range(0x30, 0x3a)] + ['a', 'b', 'c', 'd']
TAG_INFO = ['0', '1PN', '2PN', '3PN', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '>=8C', 'BC', 'EBC']

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--images', help='图像目录的路径', required=True)
    parser.add_argument('-a', '--annotation', help='标注文件路径及文件名', required=True)
    conf = parser.parse_args()
    print(TAG_MESSAGE)
    img_files = list(sorted(filter(lambda x: x.endswith('.jpg'), os.listdir(conf.images))))
    if not img_files or not len(img_files):
        print('图像目录不存在或不包含任何图像文件')
    end = False
    try:
        fn = open(conf.annotation, 'w')
        tags = []
        index = 0
        while index < len(img_files):
            f = img_files[index]
            tag = ''
            window = cv2.namedWindow('Embryo stage annotation')
            img = cv2.imread(conf.images + os.path.sep + f, cv2.IMREAD_GRAYSCALE)
            percentage = f'{index/len(img_files)*100:02d}'
            box, _ = cv2.getTextSize(percentage, cv2.FONT_HERSHEY_COMPLEX, 0.6, 1)
            img = cv2.putText(img, percentage, (20+box[0], box[1]+15), cv2.FONT_HERSHEY_COMPLEX, 
                0.6, (0,0,255), 1, cv2.LINE_AA)
            if img is None or img.shape != (600, 600):
                img_files.remove(f)
                continue
            cv2.imshow('Embryo stage annotation', img)
            while True:
                key = cv2.waitKey(100) & 0xff
                if key == 0x51 or key == 0x71 or key == 0x1B:
                    end = True
                    break
                elif key == 0x4e or key == 0x6e:
                    line = f + ' ' + str(tag) + '\n'
                    if index >= len(tags):
                        tags.append(line)
                    else:
                        tags[index] = line
                    index += 1
                    break
                elif key == 0x50 or key == 0x70:
                    if index > 0:
                        index -= 1
                        break
                elif key == 0x20:
                    tag = ''
                    index += 1
                    break
                else:
                    key = str(chr(key)).lower()
                    if key in TAG_KEYS:
                        tag = TAG_KEYS.index(key)
                        box, _ = cv2.getTextSize(TAG_INFO[tag], cv2.FONT_HERSHEY_COMPLEX, 0.8, 1)
                        img1 = img.copy()
                        img1 = cv2.putText(img1, TAG_INFO[tag], (600-20-box[0], box[1]+10), cv2.FONT_HERSHEY_COMPLEX, 
                            0.8, (0,0,255), 1, cv2.LINE_AA)
                        cv2.imshow('Embryo stage annotation', img1)
            if end:
                break
    finally:
        fn.writelines(tags)
        fn.close()

