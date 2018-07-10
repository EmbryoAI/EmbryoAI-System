# -*- coding: utf8 -*-
from entity.RestResult import RestResult
from entity.Feedback import Feedback
import dao.front.feedback_mapper as feedback_mapper
from flask import request, jsonify
from common import uuid
import time

#根据输入框的值查询患者姓名
def save_feedback(args):
    biochem_pregnancy = args["biochem_pregnancy"]
    clinical_pregnancy = args["clinical_pregnancy"]
    fetus_count = args["fetus_count"]
    user_id = args["user_id"]
    procedureId = args["procedureId"]
    createTime = updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
    
    feedback = Feedback(procedureId=procedureId, biochemPregnancy=biochem_pregnancy,
                        clinicalPregnancy=clinical_pregnancy,fetusCount=fetus_count,
                        userId=user_id,createTime=createTime,updateTime=updateTime,delFlag=0)
    
    try:
        feedback_mapper.insertFeedback(feedback)
    except:
        return 500, '保存病历回访数据错误!'
    return 200, '保存病历回访数据成功!'

def getFeedbackInfo(id):
    return feedback_mapper.getFeedbackInfo(id)