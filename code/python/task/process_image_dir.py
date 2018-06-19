# -*- coding: utf8 -*-

from ini_parser import ConfigParser
# from app import conf
from numba import jit
import numpy as np
from ImageSharpnessTool import ImageSharpnessTool
from TimeSeries import TimeSeries
import os, json, cv2

def calculate_sharpness(imfile, algorithm='lap'):
    if algorithm not in ('lap', 'smd', 'sobel'):
        raise ValueError('清晰度度量值算法应该为lap, smd或sobel')
    img = cv2.imread(imfile, cv2.IMREAD_GRAYSCALE)
    ist = ImageSharpnessTool(img)
    if algorithm == 'smd':
        return ist.sharpness_smd()
    elif algorithm == 'sobel':
        return ist.sharpness_sobel()
    else:
        return ist.sharpness_lap()

def process_well(timeserie_path, well_id, start_index, zcount, algorithm='lap'):
    img_names = np.array([timeserie_path + os.path.sep + '%05d.jpg' %i 
            for i in range(start_index, start_index+zcount)])
    img_qtys = np.array(list(map(lambda x: calculate_sharpness(x, algorithm), img_names)))
    best_qty = img_qtys.argmax()
    return well_id, img_names[best_qty]

@jit
def process_dish(dish_path, dish_id, well_info_list, reindex=False):
    json_info_file = dish_path + os.path.sep + 'dish_process_info_smd.json'
    dish_json = []
    timeserie_index = 0
    if os.path.exists(json_info_file) and not reindex:
        fn = open(json_info_file, 'r')
        dish_json = json.loads(fn.read())
        fn.close()
        timeserie_index = len(dish_json)
    ts = TimeSeries()
    if timeserie_index:
        ts.move_to(timeserie_index)
    while True:
        frame = ts.next()
        frame_path = dish_path + os.path.sep + frame
        if not os.path.exists(frame_path):
            break
        start_index = 1
        well_infos = {}
        for well_id, zcount in well_info_list:
            wid, im_path = process_well(frame_path, well_id, start_index, zcount, 'smd')
            well_infos[str(wid)] = im_path
            start_index += zcount
        dish_json.append(well_infos)
    fn = open(json_info_file, 'w')
    fn.write(json.dumps(dish_json))
    fn.close()
    mk_video(dish_path, '5', dish_json)

def mk_video(dish_path, well_id, dish_json, size=(1280, 960), codec='avi'):
    from TimeSeries import serie_to_time
    fourcc = cv2.VideoWriter_fourcc(*'DIVX') if codec=='avi' else cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(dish_path + os.path.sep + well_id + '_smd.mp4', fourcc, 5, size)
    ts = TimeSeries()
    for frame in dish_json:
        f = ts.next()
        h, m = serie_to_time(f)
        text = '%02d H %02d M' %(h, m)
        font_size = size[0]/1280
        box, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, font_size, 1)
        img = cv2.imread(frame[well_id])
        img = cv2.resize(img, size)
        img = cv2.putText(img, text, (size[0]-20-box[0], box[1]+10), cv2.FONT_HERSHEY_COMPLEX, 
            font_size, (0,0,255), 1, cv2.LINE_AA)
        video.write(img)
    video.release()

process_dish('/Users/wangying/git/repos/EmbryoAI-System/models/demo0/20170624151700/DISH1/', 1, [(5, 11)], reindex=False)
