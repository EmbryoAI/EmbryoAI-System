#!/bin/env python
# -*- coding: utf8 -*-

from argparse import ArgumentParser
import numpy as np
import cv2
from traceback import print_exc

from task.process_image_dir import process_dish, subdir_list
from configparser import ConfigParser
import os
from well_info import WellInfo

def read_dish_info(path):
    cp = ConfigParser()
    cp.read(path + os.path.sep + 'DishInfo.ini', encoding='Shift_JIS')
    dishes = int(cp['Timelapse']['DishCount'])
    wells = int(cp['Timelapse']['WellCount'])
    all_dishes = {}
    for i in range(1, dishes+1):
        all_wells = []
        dishname = f'Dish{i}Info'
        if dishname not in cp:
            continue
        for j in range(1, wells+1):
            wellavail = f'Well{j}Avail'
            if wellavail not in cp[dishname]:
                continue
            if int(cp[dishname][wellavail]) == 0:
                continue
            zcount = int(cp[dishname][f'Well{j}ZCount'])
            zslcie = int(cp[dishname][f'Well{j}ZSliceUm'])
            all_wells.append(WellInfo(str(j), zcount, zslcie))
        all_dishes[str(i)] = all_wells
    return all_dishes, cp

def process_focus(json_file, cascade, out_path):
    import json
    from embryo_focus import find_embryo
    from task.TimeSeries import TimeSeries
    with open(json_file) as fn:
        jsonstr = fn.read()
    sources = json.loads(jsonstr)
    index = 0
    serie = TimeSeries()
    for dirs in sources:
        timetag = serie.next()
        for well_id, ts in dirs.items():
            imgfile = ts
            try :
                img = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
                thumb = find_embryo(img, cascade, imgfile)
                out_file = out_path + os.path.sep + well_id + '_' + timetag + '_focus.jpg'
                cv2.imwrite(out_file, thumb, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            except:
                print_exc()

def process_edge(thumb_path, out_path):
    from cv.embryo_common import outer_edge, cell_edge
    files = os.listdir(thumb_path)
    for img_file in files:
        img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
        o_edge, o_area, o_diameter = outer_edge(img)
        i_result = cell_edge(img)
        img = to_BGR(img)
        if len(o_edge):
            img = cv2.drawContours(img, [o_edge], 0, (255,0,0), 2)
            img = cv2.putText(img, f'Outer area: {o_area:.1f} um2', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
            img = cv2.putText(img, f'Outer diameter: {o_diameter:.1f} um', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
        if len(i_result) == 1:
            i_edge, i_area, i_diameter = i_result[0]
            img = cv2.drawContours(img, [i_edge], 0, (0,255,0), 1)
            img = cv2.putText(img, f'Cell area: {i_area:.1f} um2', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
            img = cv2.putText(img, f'Cell diameter: {i_diameter:.1f} um', (10, 80), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
            thick = (o_diameter - i_diameter)/2*0.8
            img = cv2.putText(img, f'Zona thickness: {thick:.1f} um', (10, 100), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
        elif len(i_result) == 2:
            (ie0, ia0, id0), (ie1, ia1, id1) = i_result
            img = cv2.drawContours(img, [ie0], 0, (0,255,0), 1)
            img = cv2.drawContours(img, [ie1], 0, (0,0,255), 1)
            img = cv2.putText(img, f'Blastocyst area: {ia0:.1f} um2', (10, 60), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
            img = cv2.putText(img, f'Blastocyst diameter: {id0:.1f} um', (10, 80), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
            img = cv2.putText(img, f'Expansion area: {ia1:.1f} um2', (10, 100), cv2.FONT_HERSHEY_COMPLEX, 
                                0.4, (0,0,0), 1, cv2.LINE_AA)
        out_file = img_file[:-10] + '_edge.jpg'
        cv2.imwrite(out_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

def dup_img(json_file, out_path, cycle_id, dish_id):
    import json, shutil
    from task.TimeSeries import TimeSeries
    sources = json.loads(open(json_file).read())
    ts = TimeSeries()
    for serie in sources:
        nt = ts.next()
        for well_id, img_file in serie.items():
            out_file = f'{out_path}{os.path.sep}{cycle_id}_{dish_id}_{well_id}_{nt}.jpg'
            shutil.copy(img_file, out_file)

if __name__=='__main__':
    ap = ArgumentParser()
    ap.add_argument('-i', '--input', help='采集图像目录', required=True)
    ap.add_argument('-o', '--output', help='缩略图像输出目录', required=False)
    ap.add_argument('-c', '--cascade', help='胚胎定位cascde文件路径', required=False)
    ap.add_argument('-e', '--edge', help='胚胎边缘检测输出路径', required=False)
    ap.add_argument('-m', '--move', help='将清晰胚胎图像移到的目标目录', required=False)
    conf = ap.parse_args()
    path = conf.input
    if not os.path.exists(path) or not os.path.isdir(path):
        print('错误：-i --input 参数必须为一个采集图像的目录')
        exit(-1)
    all_cycles = subdir_list(path)
    for cycle in all_cycles:
        cycle_path = path + os.path.sep +cycle
        print('正在处理采集目录：'+cycle_path)
        all_dishes, base_infos = read_dish_info(cycle_path)
        for dish_id in all_dishes:
            dish_path = cycle_path + os.path.sep + 'Dish' + dish_id
            well_info = [(well.index, well.zCount) for well in all_dishes[dish_id]]
            process_dish(dish_path, dish_id, well_info, reindex=False)
            json_file = dish_path + os.path.sep + 'dish_process_info_smd.json'
            if conf.move:
                move_dir = conf.move + os.path.sep + cycle + os.path.sep + dish_id
                if not os.path.exists(move_dir):
                    os.makedirs(move_dir)
                dup_img(json_file, move_dir, cycle, dish_id)
            if conf.output:
                focus_dir = conf.output + os.path.sep + cycle + os.path.sep + dish_id
                if not os.path.exists(focus_dir):
                    os.makedirs(focus_dir)
                if not conf.cascade:
                    print('错误：指定缩略图输出后必须指定cascade文件路径, -c --cascade')
                    exit(-2)
                process_focus(json_file, conf.cascade, focus_dir)
                if conf.edge:
                    edge_dir = conf.edge + os.path.sep + cycle + os.path.sep + dish_id
                    if not os.path.exists(edge_dir):
                        os.makedirs(edge_dir)
                    process_edge(focus_dir, edge_dir)
        print('处理完成...')

