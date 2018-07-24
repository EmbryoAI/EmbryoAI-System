# -*- coding: utf8 -*-

from entity.Milestone import Milestone
from entity.MilestoneData import MilestoneData
from entity.RestResult import RestResult
import dao.front.milestone_mapper as milestone_mapper
import dao.front.milestone_data_mapper as milestone_data_mapper
from flask import request, jsonify
from common import parse_date
from common import uuid
import re
import time
from app import current_user

def insertMilestone(request):
    id = uuid()
    
    
    #胚胎ID
    embryoId = request.form.get('embryoId')
    if embryoId == "":
       return 400, '胚胎ID不能为空!'
   
    #里程碑节点ID
    milestoneId = request.form.get('milestoneId')
    if milestoneId == "":
       return 400, '里程碑节点ID不能为空!'
   
    #里程碑节点时间
    milestoneTime = request.form.get('milestoneTime')
    
    #里程碑时间点距离初次采集时间的间隔，单位分钟
    milestoneElapse = 1
    
    userId = current_user.id
    
    #里程碑时间点类型：0-自动识别；1-用户设定
    milestoneType = 1
    
    #里程碑时间点图像文件路径
    milestonePath = "milestone_path"
   
    #里程碑时间点距离授精时间的间隔，单位分钟
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
    
    create_time = update_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
 
    milestone = Milestone(id=id, embryoId=embryoId,milestoneId=milestoneId,milestoneTime=milestoneTime,milestoneElapse=milestoneElapse,
                          userId=userId,milestoneType=milestoneType,milestonePath=milestonePath)
    
    milestoneData = MilestoneData(milestoneId=id, milestoneStage=milestoneStage,pnId=pnId,cellCount=cellCount,evenId=evenId,
                      fragmentId=fragmentId,gradeId=gradeId,diameter=diameter,area=area,thickness=thickness,milestoneScore=milestoneScore
                      ,userId=userId,memo=memo)
    
    try:
        #根据胚胎ID和的里程碑的图片查出是否已经存在了
        sql = "AND embryo_id = :embryoId and milestone_path = :milestonePath "
        filters = {'embryoId': embryoId,'milestonePath':milestonePath}
        milestoneOld = milestone_mapper.getMilestoneByEmbryoId(sql,filters)
        if not milestoneOld:
            milestone_mapper.insertMilestone(milestone,milestoneData)
        else:
            milestone.id = milestoneOld.id;
            milestoneData.milestoneId = milestoneOld.id;
            milestone_mapper.updateMilestone(milestone,milestoneData)
    except:
        return 400, '设置里程碑时异常!'
    return 200, milestone.to_dict()

def getMilestoneByEmbryoId(embryoId):
    try: 
        sql = "AND embryo_id = :embryoId"
        filters = {'embryoId': embryoId}
        milestone = milestone_mapper.getMilestoneByEmbryoId(sql,filters)
        if milestone!=None:
            milestoneData = milestone_data_mapper.getMilestoneData(milestone.id)
            result = {}
            result["milestone"] = dict(milestone)
            result["milestoneData"] = milestoneData.to_dict()
        restResult = RestResult(0, "404", 0, None)
        if milestone is not None:
            restResult = RestResult(0, "OK", 1, result)
        return jsonify(restResult.__dict__)
    except:
        return 400, '查询里程碑详情时发生错误!'