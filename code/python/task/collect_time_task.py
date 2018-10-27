from app import app,conf
import dao.front.procedure_mapper as procedure_mapper
import json,datetime
import os
import service.front.image_service as image_service
from common import logger
'''
### 定时任务模块，flask-scheduler通过调用run方法采集任务。
#### 定时任务需要完成的工作包括：
- 查询数据库周期表（t_procedure）采集结束时间字段（cap_end_time）为空的采集目录
- 判断采集目录是否已经采集完成（finished_cycles.json），如果采集完成则把完成时间写回数据库
 
'''

logger = app.logger
finished_json = conf['FINISHED_JSON_FILENAME'] # 已完成的采集目录列表JSON文件名称
path = conf['EMBRYOAI_IMAGE_ROOT'] #采集目录
def run():
    ''' 定时任务【同步采集时间】入口方法 '''
    json_file = path + finished_json # 存储结束采集目录列表的JSON文件
    with open(json_file) as fn:
        finished = json.load(fn) # 文件存在则读取文件的内容
    
    collectList = procedure_mapper.queryCollectList()
    flag = False
    for collect in collectList:#判断 字段为空的结束采集时间 的采集目录  是否已经采集完成了
        for fini in finished:
            if collect["imagePath"]==fini:
                flag = True
                break
        
        if flag:#采集完成了 才把采集结束时间 同步到数据库
           capStartTime = datetime.datetime.strptime(collect["imagePath"], "%Y%m%d%H%M%S")#把采集目录转换为 日期
           #获取当前采集目录下的最后一个时间序列
           a,b,dishJson = image_service.readDishState(collect["procedureId"],collect["dishId"])
           
           seriesList = []
           if dishJson['finished'] & dishJson['avail'] == 1 : 
                wells = dishJson['wells']
                for i in range(1,12):
                    try:
                        oneWell = wells[f'{i}']
                        series = oneWell['series']
                        for key in series:
                            seriesList.append(key)
                    except e:
                         seriesList = seriesList
           timeSeries = max(seriesList)
           print(timeSeries)
           #开始时间+时间序列的时间  使用datetime.timedelta方法 
           capEndtime = (capStartTime+datetime.timedelta(days=int(timeSeries[0:1]))
            +datetime.timedelta(hours=int(timeSeries[1:3]))+datetime.timedelta(minutes=int(timeSeries[3:5]))
            +datetime.timedelta(seconds=int(timeSeries[5:7])))
           
           
           
           #把计算好的采集开始时间 和 结束时间入库
           procedure_mapper.updateCollect(collect["procedureId"],capStartTime,capEndtime)
    logger.debug('结束定时任务')