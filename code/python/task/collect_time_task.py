from app import app, conf
import dao.front.procedure_mapper as procedure_mapper
import json, datetime
import os
import service.front.image_service as image_service
from common import scheduler  # 很关键的一步，导入初始化过的sheduler对象---为了定时任务获取到上下文
import logUtils

"""
### 定时任务模块，flask-scheduler通过调用run方法采集任务。
#### 定时任务需要完成的工作包括：
- 查询数据库周期表（t_procedure）采集结束时间字段（cap_end_time）为空的采集目录
- 判断采集目录是否已经采集完成（finished_cycles.json），如果采集完成则把完成时间写回数据库
 
"""
finished_json = conf["FINISHED_JSON_FILENAME"]  # 已完成的采集目录列表JSON文件名称
path = conf["EMBRYOAI_IMAGE_ROOT"]  # 采集目录


def run():
    with scheduler.app.app_context():  # 这个sheduler是带有app及其上下文的 ---为了定时任务获取到上下文
        """ 定时任务【同步采集时间】入口方法 """
        json_file = path + finished_json  # 存储结束采集目录列表的JSON文件
        try:
            with open(json_file) as fn:
                finished = json.load(fn)  # 文件存在则读取文件的内容
        except:
            return

        collectList = procedure_mapper.queryCollectList()
        if len(collectList):
            for collect in collectList:  # 判断 字段为空的结束采集时间 的采集目录  是否已经采集完成了
                listnew = list(filter(lambda x: collect["imagePath"] in x, finished))
                if len(listnew):
                    flag = listnew[0][collect["imagePath"]]
                    #         for fini in:(NULL)
                    #            for fini in finished:
                    #              if collect["imagePath"]==fini:
                    #                 flag = True
                    #                 break

                    if flag:  # 采集完成了 才把采集结束时间 同步到数据库
                        capStartTime = datetime.datetime.strptime(
                            collect["imagePath"], "%Y%m%d%H%M%S"
                        )  # 把采集目录转换为 日期
                        # 获取当前采集目录下的最后一个时间序列
                        a, b, dishJson = image_service.readDishState(
                            collect["procedureId"], collect["dishId"]
                        )

                        # 循环所有孔的时间序列，保存起来，取最大的一个
                        seriesList = []
                        if dishJson["finished"] & dishJson["avail"] == 1:
                            wells = dishJson["wells"]
                            for i in range(1, 12):
                                try:
                                    oneWell = wells[f"{i}"]
                                    series = oneWell["series"]
                                    for key in series:
                                        seriesList.append(key)
                                except Exception as e:
                                    seriesList = seriesList
                        timeSeries = max(seriesList)  # 取最大的一个

                        # 开始时间+时间序列的时间  使用datetime.timedelta方法
                        capEndtime = (
                            capStartTime
                            + datetime.timedelta(days=int(timeSeries[0:1]))
                            + datetime.timedelta(hours=int(timeSeries[1:3]))
                            + datetime.timedelta(minutes=int(timeSeries[3:5]))
                            + datetime.timedelta(seconds=int(timeSeries[5:7]))
                        )

                        # 把计算好的采集开始时间 和 结束时间入库
                        procedure_mapper.updateCollect(
                            collect["procedureId"], capStartTime, capEndtime
                        )
                        logUtils.debug("定时任务【同步采集时间】结束")
                else:
                    logUtils.debug("定时任务【同步采集时间】结束，listnew值为空")
        else:
            logUtils.debug("定时任务【同步采集时间】结束，没有需要同步的数据")
