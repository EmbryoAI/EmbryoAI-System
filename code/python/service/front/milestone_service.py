# -*- coding: utf8 -*-

from entity.Milestone import Milestone
from entity.MilestoneData import MilestoneData
from entity.RestResult import RestResult
import dao.front.milestone_mapper as milestone_mapper
import dao.front.milestone_data_mapper as milestone_data_mapper
import dao.front.procedure_mapper as procedure_mapper
from flask import request, jsonify
from common import parse_date
from common import uuid
import re
import time
import datetime
from traceback import print_exc
from app import current_user, conf
import service.front.image_service as image_service
import logUtils


def insertMilestone(request):
    id = uuid()

    # 胚胎ID
    embryoId = request.form.get("embryoId")
    if not embryoId:
        return 400, "胚胎ID不能为空!"

    # 周期ID
    procedureId = request.form.get("procedureId")
    if not procedureId:
        return 400, "周期ID不能为空!"

    # 里程碑节点ID  对应字典值
    milestoneId = request.form.get("milestoneId")
    if not milestoneId:
        return 400, "里程碑节点ID不能为空!"

    # 里程碑时间（自动识别或用户设定的里程碑时间点）时间序列
    milestoneTime = request.form.get("timeSeries")

    # 目前暂不使用
    milestoneElapse = 1

    userId = current_user.id

    # 里程碑时间点类型：0-自动识别；1-用户设定
    milestoneType = 1

    # 里程碑时间点图像文件路径
    milestonePath = request.form.get("milestonePath")
    if not milestonePath:
        return 400, "图片路径不能为空!"
    # 获取缩略图
    thumbnailPath = request.form.get("thumbnailPath")

    procedure = procedure_mapper.getProcedure(procedureId)
    # 根据周期ID获取受精时间

    # 里程碑时间点距离授精时间的间隔，单位分钟    采集时间+时间序列-授精时间算成分钟数
    timeSeries = request.form.get("timeSeries")
    cap_start_time = request.form.get("milestoneStage")
    milestoneStage = request.form.get("milestoneStage")
    milestoneStage = datetime.datetime.strptime(milestoneStage, "%Y%m%d%H%M%S")
    milestoneStage = (
        milestoneStage
        + datetime.timedelta(days=int(timeSeries[0:1]))
        + datetime.timedelta(hours=int(timeSeries[1:3]))
        + datetime.timedelta(minutes=int(timeSeries[3:5]))
        + datetime.timedelta(seconds=int(timeSeries[5:7]))
    )
    milestoneStage = milestoneStage - procedure.insemiTime
    milestoneStage = int(round(milestoneStage.total_seconds() / 60, 1))
    #     c = a+b
    #     d = c+datetime.datetime.strptime("0160000", '%d%H:%M:%S')
    #
    #     print(c)

    # PN数量字典值ID -> sys_dict.id，字典值类型为pn，可能取值：0：0PN；1：1PN；2：2PN；3：>=3PN
    pnId = request.form.get("pnId")

    # 细胞数
    cellCount = request.form.get("count")

    # 细胞是否均匀字典值ID -> sys_dict.id，字典值类型为even，可能取值：0：均匀；1：不均匀
    evenId = request.form.get("evenId")

    # 碎片比例
    fragmentId = request.form.get("fragmentId")

    # 胚胎评级
    gradeId = request.form.get("gradeId")

    # 胚胎直径，单位um
    innerDiameter = request.form.get("innerDiameter")

    # 胚胎面积，单位平方um
    innerArea = request.form.get("innerArea")

    # 透明带厚度，单位um
    zonaThickness = request.form.get("zonaThickness")

    # 里程碑时间点得分
    milestoneScore = request.form.get("milestoneScore")

    # 备注
    memo = request.form.get("memo")

    # 胚胎外面积
    outerArea = request.form.get("outerArea")

    # 胚胎外直接
    outerDiameter = request.form.get("outerDiameter")

    # 扩张囊腔面积
    expansionArea = request.form.get("expansionArea")

    #     create_time = update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

    milestone = Milestone(
        id=id,
        embryoId=embryoId,
        milestoneId=milestoneId,
        milestoneTime=milestoneTime,
        milestoneElapse=milestoneElapse,
        userId=userId,
        milestoneType=milestoneType,
        milestonePath=milestonePath,
        thumbnailPath=thumbnailPath,
    )

    milestoneData = MilestoneData(
        milestoneId=id,
        milestoneStage=milestoneStage,
        pnId=pnId,
        cellCount=cellCount,
        evenId=evenId,
        fragmentId=fragmentId,
        gradeId=gradeId,
        innerDiameter=innerDiameter,
        innerArea=innerArea,
        zonaThickness=zonaThickness,
        milestoneScore=milestoneScore,
        userId=userId,
        memo=memo,
        outerArea=outerArea,
        outerDiameter=outerDiameter,
        expansionArea=expansionArea,
    )

    try:
        # 根据胚胎ID和的里程碑的图片查出是否已经存在了,存在则更新
        sql = "AND embryo_id = :embryoId and milestone_time = :milestoneTime "
        filters = {"embryoId": embryoId, "milestoneTime": milestoneTime}
        milestoneOld = milestone_mapper.getMilestoneByEmbryoId(sql, filters)
        milestoneScoreResult = 0
        embryoScoreResult = 0
        if not milestoneOld:
            # 根据胚胎ID和里程碑值查询是否存在了，存在则把当前里程碑节点替换成当前图片
            sql = "AND embryo_id = :embryoId and milestone_id = :milestoneId "
            filters = {"embryoId": embryoId, "milestoneId": milestoneId}
            milestoneOld = milestone_mapper.getMilestoneByEmbryoId(sql, filters)
            if not milestoneOld:
                (
                    milestoneScoreResult,
                    embryoScoreResult,
                ) = milestone_mapper.insertMilestone(
                    milestone, milestoneData, procedure, cap_start_time
                )
            else:
                milestone.id = milestoneOld.id
                milestoneData.milestoneId = milestoneOld.id
                (
                    milestoneScoreResult,
                    embryoScoreResult,
                ) = milestone_mapper.updateMilestone(
                    milestone, milestoneData, procedure, cap_start_time
                )
        else:
            milestone.id = milestoneOld.id
            milestoneData.milestoneId = milestoneOld.id
            milestoneScoreResult, embryoScoreResult = milestone_mapper.updateMilestone(
                milestone, milestoneData, procedure, cap_start_time
            )
        result = {
            "milestoneScore": milestoneScoreResult,
            "embryoScore": embryoScoreResult,
        }
    #         '''由于字典转换太过麻烦，目前采用这种不合理方式实现，后续优化'''
    #         #评分设置，首先查询出当前周期对应的评分规则
    #         rule = rule_dao.getRuleById(procedure.embryoScoreId,userId)
    #         engine = embryo_score.init_engine(rule.dataJson)
    #         #获取当前胚胎的所有里程碑节点的胚胎形态
    #         embryoForm = milestone_mapper.queryEmbryoForm(embryoId)
    # #         embryoFormList = list(map(dict, embryoForm))
    #         sumScore = 0;
    #         for obj in embryoForm:
    #             engine = embryo_score.init_engine(rule.dataJson)
    #             cap_start_time = request.form.get('milestoneStage')
    #             cap_start_time = datetime.datetime.strptime(cap_start_time, "%Y%m%d%H%M%S")
    #             cap_start_time = cap_start_time.strftime("%Y-%m-%d %H:%M")
    #             insemiTime = procedure.insemiTime.strftime("%Y-%m-%d %H:%M")
    #             timeValue = get_serie_time_hours(insemiTime,cap_start_time,obj.milestoneTime)
    #             #计算时间
    #             engine.declare(Fact(stage=obj.stage,condition="time", value=str(timeValue)))
    #             #计算节点
    #             if obj.stage == 'PN':
    #                 engine.declare(Fact(stage=obj.stage,condition=obj.condition, value=obj.value))
    #             elif obj.stage=="2C" or obj.stage=="3C" or obj.stage=="4C" or obj.stage=="5C" or obj.stage=="8C":
    #                  engine.declare(Fact(stage=obj.stage,condition=obj.condition1, value=obj.value1))
    #                  engine.declare(Fact(stage=obj.stage,condition=obj.condition2, value=obj.value2))
    #                  if obj.stage=="3C" or obj.stage=="4C" or obj.stage=="5C" or obj.stage=="8C":
    #                     engine.declare(Fact(stage=obj.stage,condition=obj.condition3, value=obj.value3))
    #                  if obj.stage=="8C":
    #                     engine.declare(Fact(stage=obj.stage,condition=obj.condition4, value=obj.value4))
    #             engine.run()
    #             sumScore+=engine.score
    #             print(engine.score)
    #         print(sumScore)
    #         embryo_mapper.updateEmbryoScore(embryoId,sumScore)
    except:
        print_exc()
        return 400, "设置里程碑时异常!"

    # 读取上传云端代码块开关
    switch = conf["CLOUD_CODE_SWITCH"]
    if switch:
        try:
            # 同步里程碑到云端-开启异步线程同步
            import threading

            thread = threading.Thread(target=nsync, args=(milestone, milestoneData))
            thread.start()
        except:
            logUtils.info("同步里程碑到云端异常")

    return 200, result


def nsync(milestone, milestoneData):
    import json
    from app import conf
    from common import request_post
    import dao.front.dict_dao as dict_dao

    url = conf["MILESTONE_INFO_UP_URL"]
    # 里程碑字典转换
    milestoneDict = dict_dao.getDictByClassAndKey("milestone", milestone.milestoneId)
    milestone.milestoneId = milestoneDict.dictValue
    if milestoneData.pnId != None:
        # PN字典转换
        pnDict = dict_dao.getDictByClassAndKey("pn", milestoneData.pnId)
        milestoneData.pnId = pnDict.dictValue
    # 均匀度
    evenDict = dict_dao.getDictByClassAndKey("even", milestoneData.evenId)
    milestoneData.evenId = evenDict.dictValue
    # 碎片比例字典转换
    fragmentDict = dict_dao.getDictByClassAndKey("fragment", milestoneData.fragmentId)
    milestoneData.fragmentId = fragmentDict.dictValue
    # 胚胎评级字典转换
    gradeDict = dict_dao.getDictByClassAndKey("grade", milestoneData.gradeId)
    milestoneData.gradeId = gradeDict.dictValue

    baseResult = {
        "milestone": milestone.to_dict(),
        "milestoneData": milestoneData.to_dict(),
    }
    request_post(url, json.dumps(baseResult, ensure_ascii=False))


def getMilestoneByEmbryoId(embryoId, timeSeries, procedureId, dishId, wellId):
    if not timeSeries:
        return 400, "初始化里程碑节点出错，图片路径不能为空!"
    try:
        sql = "AND embryo_id = :embryoId and milestone_time = :milestoneTime "
        filters = {"embryoId": embryoId, "milestoneTime": timeSeries}
        milestone = milestone_mapper.getMilestoneByEmbryoId(sql, filters)
        milestoneData = None
        result = {}
        if milestone != None:
            milestoneData = milestone_data_mapper.getMilestoneData(milestone.id)

            result["milestone"] = dict(milestone)
            result["milestoneData"] = milestoneData.to_dict()

        if milestoneData is None:
            result["milestoneData"] = analysisMilestoneData(
                procedureId, dishId, timeSeries, wellId
            )

        if not result:
            return 200, None
        else:
            return 200, result
    except:
        return 400, "初始化里程碑节点出错!"


def analysisMilestoneData(procedureId, dishId, timeSeries, wellId):
    imagePath, path, dishJson = image_service.readDishState(procedureId, dishId)
    return dishJson["wells"][wellId]["series"][timeSeries]


def getMilepostNode(embryoId, milestoneTime, upOrdown):
    try:
        # 首先获取当前胚胎的所有里程碑节点
        milestoneList = milestone_mapper.queryMilestoneList(embryoId)
        if "up" == upOrdown:  # 如果为上一里程碑集合反转
            milestoneList.reverse()

        milestone = None
        for obj in milestoneList:
            logUtils.info(obj.milestoneTime)
            if "up" == upOrdown:  # 如果是上一里程碑
                if obj.milestoneTime < milestoneTime:
                    milestone = obj.to_dict()
                    break
            else:
                if obj.milestoneTime > milestoneTime:
                    milestone = obj.to_dict()
                    break
        return 200, milestone
    except:
        return 400, "获取上下里程碑节点出错!"


def getMilestone(agrs):
    procedure_id = agrs["procedureId"]
    cell_id = agrs["cellId"]

    embryo = embryo_mapper.queryByProcedureIdAndCellId(procedure_id, cell_id)
    milestone_list = milestone_mapper.getMilestone(embryo.id)
    list = []
    for milestone in milestone_list:
        logUtils.info(f"milestone:{milestone}")
        obj = {}
        obj["milestoneType"] = milestone.milestone_type
        obj["embryoId"] = milestone.embryo_id
        obj["seris"] = milestone.seris
        list.append(obj)
    return jsonify(list)
