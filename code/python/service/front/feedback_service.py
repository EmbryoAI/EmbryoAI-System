# -*- coding: utf8 -*-
from entity.RestResult import RestResult
from entity.Feedback import Feedback
import dao.front.feedback_mapper as feedback_mapper
from flask import request, jsonify
from common import uuid
import time

# 根据输入框的值查询患者姓名
def save_feedback(request):
    biochem_pregnancy = request.json.get("biochem_pregnancy")
    clinical_pregnancy = request.json.get("clinical_pregnancy")
    fetus_count = request.json.get("fetus_count")
    user_id = request.json.get("user_id")
    procedure_id = request.json.get("procedure_id")
    createTime = updateTime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
    )

    feedback = Feedback(
        procedureId=procedure_id,
        biochemPregnancy=biochem_pregnancy,
        clinicalPregnancy=clinical_pregnancy,
        fetusCount=fetus_count,
        userId=user_id,
        createTime=createTime,
        updateTime=updateTime,
        delFlag=0,
    )

    try:
        feedback_mapper.insertFeedback(feedback)
    except:
        return 500, "保存病历回访数据错误!"
    return 200, "保存病历回访数据成功!"


def getFeedbackInfo(id):
    return feedback_mapper.getFeedbackInfo(id)
