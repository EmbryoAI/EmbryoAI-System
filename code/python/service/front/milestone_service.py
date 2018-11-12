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
from common import get_serie_time_minutes_new
import re
import time
import datetime
from app import current_user
import service.front.image_service as image_service
import dao.front.rule_dao as rule_dao
import dao.front.embryo_mapper as embryo_mapper
import knowledge.embryo_score as embryo_score
from pyknow import *
from functools import partial

def insertMilestone(request):
    id = uuid()
    
    
    #胚胎ID
    embryoId = request.form.get('embryoId')
    if not embryoId:
       return 400, '胚胎ID不能为空!'
   
    #周期ID
    procedureId = request.form.get('procedureId')
    if not procedureId:
       return 400, '周期ID不能为空!'
   
   
    #里程碑节点ID  对应字典值
    milestoneId = request.form.get('milestoneId')
    if not milestoneId:
       return 400, '里程碑节点ID不能为空!'
   
    #里程碑时间（自动识别或用户设定的里程碑时间点）时间序列
    milestoneTime = request.form.get('timeSeries')
    
    #目前暂不使用
    milestoneElapse = 1
    
    userId = current_user.id
    
    #里程碑时间点类型：0-自动识别；1-用户设定
    milestoneType = 1
    
    #里程碑时间点图像文件路径
    milestonePath = request.form.get('milestonePath')
    if not milestonePath:
       return 400, '图片路径不能为空!'
    #获取缩略图
    thumbnailPath = request.form.get('thumbnailPath')
    
    
    procedure = procedure_mapper.getProcedure(procedureId)
    #根据周期ID获取受精时间
    
    #里程碑时间点距离授精时间的间隔，单位分钟    采集时间+时间序列-授精时间算成分钟数
    timeSeries= request.form.get('timeSeries')
    milestoneStage = request.form.get('milestoneStage')
    milestoneStage = datetime.datetime.strptime(milestoneStage, "%Y%m%d%H%M%S")
    milestoneStage = (milestoneStage+datetime.timedelta(days=int(timeSeries[0:1]))
    +datetime.timedelta(hours=int(timeSeries[1:3]))+datetime.timedelta(minutes=int(timeSeries[3:5]))
    +datetime.timedelta(seconds=int(timeSeries[5:7])))
    milestoneStage = milestoneStage-procedure.insemiTime
    milestoneStage = int(round(milestoneStage.total_seconds()/60,1))
#     c = a+b
#     d = c+datetime.datetime.strptime("0160000", '%d%H:%M:%S')
#
#     print(c)

    #PN数量字典值ID -> sys_dict.id，字典值类型为pn，可能取值：0：0PN；1：1PN；2：2PN；3：>=3PN
    pnId = request.form.get('pnId')
    
    #细胞数
    cellCount = request.form.get('count')
    
    #细胞是否均匀字典值ID -> sys_dict.id，字典值类型为even，可能取值：0：均匀；1：不均匀
    evenId = request.form.get('evenId')
    
    #碎片比例
    fragmentId = request.form.get('fragmentId')
    
    #胚胎评级
    gradeId = request.form.get('gradeId')

    #胚胎直径，单位um
    innerDiameter = request.form.get('innerDiameter')
    
    #胚胎面积，单位平方um
    innerArea = request.form.get('innerArea')
    
    #透明带厚度，单位um
    zonaThickness = request.form.get('zonaThickness')
    
    #里程碑时间点得分
    milestoneScore = request.form.get('milestoneScore')
    
    #备注
    memo = request.form.get('memo')

    #胚胎外面积
    outerArea = request.form.get('outerArea')

    #胚胎外直接
    outerDiameter = request.form.get('outerDiameter')

    #扩张囊腔面积
    expansionArea = request.form.get('expansionArea')
    
#     create_time = update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
 
    milestone = Milestone(id=id, embryoId=embryoId,milestoneId=milestoneId,milestoneTime=milestoneTime,milestoneElapse=milestoneElapse,
                          userId=userId,milestoneType=milestoneType,milestonePath=milestonePath,thumbnailPath=thumbnailPath)
    
    milestoneData = MilestoneData(milestoneId=id, milestoneStage=milestoneStage,pnId=pnId,cellCount=cellCount,evenId=evenId,
                      fragmentId=fragmentId,gradeId=gradeId,innerDiameter=innerDiameter,innerArea=innerArea,zonaThickness=zonaThickness,milestoneScore=milestoneScore
                      ,userId=userId,memo=memo, outerArea=outerArea, outerDiameter=outerDiameter, expansionArea=expansionArea)
    
    try:
        #根据胚胎ID和的里程碑的图片查出是否已经存在了,存在则更新
        sql = "AND embryo_id = :embryoId and milestone_time = :milestoneTime "
        filters = {'embryoId': embryoId,'milestoneTime':milestoneTime}
        milestoneOld = milestone_mapper.getMilestoneByEmbryoId(sql,filters)
        if not milestoneOld:
            #根据胚胎ID和里程碑值查询是否存在了，存在则把当前里程碑节点替换成当前图片
            sql = "AND embryo_id = :embryoId and milestone_id = :milestoneId "
            filters = {'embryoId': embryoId,'milestoneId':milestoneId}
            milestoneOld = milestone_mapper.getMilestoneByEmbryoId(sql,filters)
            if not milestoneOld:
                milestone_mapper.insertMilestone(milestone,milestoneData)
            else:
                milestone.id = milestoneOld.id
                milestoneData.milestoneId = milestoneOld.id
                milestone_mapper.updateMilestone(milestone,milestoneData)
        else:
            milestone.id = milestoneOld.id
            milestoneData.milestoneId = milestoneOld.id
            milestone_mapper.updateMilestone(milestone,milestoneData)
            
        #评分设置，首先查询出当前周期对应的评分规则
        rule = rule_dao.getRuleById(procedure.embryoScoreId,userId)
        engine = embryo_score.init_engine(rule.dataJson)
        #获取当前胚胎的所有里程碑节点的胚胎形态
        embryoForm = milestone_mapper.queryEmbryoForm(embryoId)
#         embryoFormList = list(map(dict, embryoForm))
        for obj in embryoForm:
            cap_start_time = request.form.get('milestoneStage')
            timeValue = get_serie_time_minutes_new(cap_start_time,procedure.insemiTime,obj.milestoneTime)
            #计算时间
            engine.declare(Fact(stage=obj.stage,condition="time", value=str(timeValue)))
            #计算节点
            if obj.stage == 'PN':
                engine.declare(Fact(stage=obj.stage,condition=obj.condition, value=obj.value))
            elif obj.stage=="2C" or obj.stage=="3C" or obj.stage=="4C" or obj.stage=="5C" or obj.stage=="8C":    
                 engine.declare(Fact(stage=obj.stage,condition=obj.condition1, value=obj.value1))
                 engine.declare(Fact(stage=obj.stage,condition=obj.condition2, value=obj.value2))
                 if obj.stage=="3C" or obj.stage=="4C" or obj.stage=="5C" or obj.stage=="8C":
                    engine.declare(Fact(stage=obj.stage,condition=obj.condition3, value=obj.value3))
                 if obj.stage=="8C":
                    engine.declare(Fact(stage=obj.stage,condition=obj.condition4, value=obj.value4))
        engine.run()
        print(engine.score)
        embryo_mapper.updateEmbryoScore(embryoId,engine.score)
    except:
        return 400, '设置里程碑时异常!'
    return 200, '设置里程碑时成功!'

def getMilestoneByEmbryoId(embryoId, timeSeries, procedureId, dishId, wellId):
    if not timeSeries:
        return 400, '初始化里程碑节点出错，图片路径不能为空!'
    sql = "AND embryo_id = :embryoId and milestone_time = :milestoneTime "
    filters = {'embryoId': embryoId,'milestoneTime':timeSeries}
    milestone = milestone_mapper.getMilestoneByEmbryoId(sql,filters)
    milestoneData = None
    result = {}
    if milestone!=None:
        milestoneData = milestone_data_mapper.getMilestoneData(milestone.id)

        result["milestone"] = dict(milestone)
        result["milestoneData"] = milestoneData.to_dict()

    if milestoneData is None:
        result["milestoneData"] = analysisMilestoneData(procedureId, dishId, timeSeries, wellId)
        
    if not result:
        return 200, None
    else: 
        return 200, result
    

def analysisMilestoneData(procedureId, dishId, timeSeries, wellId):
    imagePath, path, dishJson = image_service.readDishState(procedureId, dishId)
    return dishJson['wells'][wellId]['series'][timeSeries]

def getMilepostNode(embryoId,milestoneTime,upOrdown):
    #首先获取当前胚胎的所有里程碑节点
    milestoneList = milestone_mapper.queryMilestoneList(embryoId)
    if "up" == upOrdown:#如果为上一里程碑集合反转
       milestoneList.reverse()
    
    milestone = None
    for obj in milestoneList:
        print(obj.milestoneTime)
        if "up" == upOrdown: #如果是上一里程碑
            if obj.milestoneTime < milestoneTime:
                milestone = obj.to_dict()
                break
        else :
            if obj.milestoneTime > milestoneTime:
                milestone = obj.to_dict()
                break
    return 200, milestone