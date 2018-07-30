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
from app import current_user

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
    milestoneTime = request.form.get('milestoneTime')
    
    #目前暂不使用
    milestoneElapse = 1
    
    userId = current_user.id
    
    #里程碑时间点类型：0-自动识别；1-用户设定
    milestoneType = 1
    
    #里程碑时间点图像文件路径
    milestonePath = request.form.get('milestonePath')
    if not milestonePath:
       return 400, '图片路径不能为空!'
    
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
    
    
    milestoneStage = ""
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
    diameter = request.form.get('diameter')
    
    #胚胎面积，单位平方um
    area = request.form.get('area')
    
    #透明带厚度，单位um
    thickness = request.form.get('thickness')
    
    #里程碑时间点得分
    milestoneScore = request.form.get('milestoneScore')
    
    #备注
    memo = request.form.get('memo')
    
#     create_time = update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
 
    milestone = Milestone(id=id, embryoId=embryoId,milestoneId=milestoneId,milestoneTime=milestoneTime,milestoneElapse=milestoneElapse,
                          userId=userId,milestoneType=milestoneType,milestonePath=milestonePath)
    
    milestoneData = MilestoneData(milestoneId=id, milestoneStage=milestoneStage,pnId=pnId,cellCount=cellCount,evenId=evenId,
                      fragmentId=fragmentId,gradeId=gradeId,diameter=diameter,area=area,thickness=thickness,milestoneScore=milestoneScore
                      ,userId=userId,memo=memo)
    
    try:
        #根据胚胎ID和的里程碑的图片查出是否已经存在了,存在则更新
        sql = "AND embryo_id = :embryoId and milestone_path = :milestonePath "
        filters = {'embryoId': embryoId,'milestonePath':milestonePath}
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
    except:
        return 400, '设置里程碑时异常!'
    return 200, milestone.to_dict()

def getMilestoneByEmbryoId(embryoId,milestonePath):
    try: 
        if not milestonePath:
           return 400, '初始化里程碑节点出错，图片路径不能为空!'
        sql = "AND embryo_id = :embryoId and milestone_path = :milestonePath "
        filters = {'embryoId': embryoId,'milestonePath':milestonePath}
        milestone = milestone_mapper.getMilestoneByEmbryoId(sql,filters)
        result = {}
        if milestone!=None:
            milestoneData = milestone_data_mapper.getMilestoneData(milestone.id)
            result["milestone"] = dict(milestone)
            result["milestoneData"] = milestoneData.to_dict()
        if not result:
            return 200, None
        else: 
            return 200, result
    except:
        return 400, '查询里程碑详情时发生错误!'