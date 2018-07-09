from argparse import ArgumentParser
import cv2
import numpy as np
import json, os
from traceback import print_exc

def find_embryo(img, cascade, imgfile):
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif img.ndim == 2:
        pass
    else:
        raise TypeError('Not an image')
    cas_template = cv2.CascadeClassifier(cascade)
    rect = cas_template.detectMultiScale(img, minSize=(500, 500)) # , maxSize=(600, 600))
    if len(rect) == 0:
        raise ValueError(f'Can not find a embryo in {imgfile}')
    if len(rect) > 1:
        raise ValueError(f'More than one embryos found in {imgfile}')
    x, y, w, h = rect[0]
    centerx, centery = x+w//2, y+h//2
    return img[centery-299:centery+301, centerx-299:centerx+301]

def save_thumb(thumb_img, path, prefix, pfile=''):
    if thumb_img.ndim == 2:
        pass
        # thumb_img = cv2.cvtColor(thumb_img, cv2.COLOR_GRAY2BGR)
    elif thumb_img.ndim == 3:
        pass
    else:
        raise ValueError('Not an image')
    file_out = path + os.sep + pfile + prefix + '_focus.jpg'
    print(f'saving to focus image file {file_out}')
    cv2.imwrite(file_out, thumb_img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', help='output dir', required=True)
    parser.add_argument('-j', '--json', help='source json file', required=True)
    parser.add_argument('-c', '--cascade', help='cascade template file', required=True)
    parser.add_argument('-p', '--prefix', help='output file name prefix', required=False)
    conf = parser.parse_args()
    if not os.path.exists(conf.json):
        print('source json file not found, exit.')
        exit(-1)
    if not os.path.exists(conf.cascade):
        print('cascade template file not found, exit.')
        exit(-1)
    if not os.path.exists(conf.output):
        print('output directory not found, create.')
        os.makedirs(conf.output)
    with open(conf.json) as fn:
        jstr = fn.read()
    sources = json.loads(jstr)
    index = 0
    for dirs in sources:
        for cell_id, ts in dirs.items():
            try :
                # imgfile = imgfile.replace('../../data/out', '/Users/wangying/docker-volumes/data/output')
                img = cv2.imread(ts, cv2.IMREAD_GRAYSCALE)
                thumb = find_embryo(img, conf.cascade, ts)
                save_thumb(thumb, conf.output, os.path.split(ts)[0][-7:], conf.prefix+cell_id+'_' if conf.prefix else cell_id)
            except ValueError:
                print_exc()
                    # base_dir, base_name = os.path.split(ts)
                    # img_index = int(base_name.split('.')[0])
                    # imgfile = f'{base_dir}{os.path.sep}{img_index-1:05d}.jpg'
                    # # print(imgfile)
                    # try :
                    #     img = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
                    #     thumb = find_embryo(img, conf.cascade, imgfile)
                    #     save_thumb(thumb, conf.output, os.path.split(imgfile)[0][-7:], conf.prefix if conf.prefix else '')
                    # except ValueError:
                    #     imgfile = f'{base_dir}{os.path.sep}{img_index+1:05d}.jpg'
                    #     try :
                    #         img = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
                    #         thumb = find_embryo(img, conf.cascade, imgfile)
                    #         save_thumb(thumb, conf.output, os.path.split(imgfile)[0][-7:], conf.prefix if conf.prefix else '')
                    #     except ValueError:
                    #         print_exc()
