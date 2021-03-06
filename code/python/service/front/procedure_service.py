# -*- coding: utf8 -*-

from entity.Procedure import Procedure
from entity.RestResult import RestResult
import dao.front.procedure_mapper as procedure_mapper
import dao.front.patient_mapper as patient_mapper
from flask import request, jsonify
from common import parse_date
import re
import time
import dao.front.dict_dao as dict_dao
from task.TimeSeries import TimeSeries, serie_to_time
from collections import OrderedDict
from app import conf
import service.front.image_service as image_service


def queryProcedureList(request):
    try:
        page = request.args.get("page")
        if page == None:
            page = 1
        limit = request.args.get("limit")
        if limit == None:
            limit = 10
        getFocus = request.args.get("getFocus")
        if getFocus == None:
            getFocus = 0

        # 动态组装查询条件
        sqlCondition = " where pr.del_flag=0 "  # 动态sql
        filters = {}  # 动态参数
        userName = request.args.get("userName")  # 用户名字
        if userName != None and userName != "":
            filters["userName"] = "%" + userName + "%"
            sqlCondition += " and pa.patient_name like :userName "

        medicalRecordNo = request.args.get("medicalRecordNo")  # 病历号
        if medicalRecordNo != None and medicalRecordNo != "":
            filters["medicalRecordNo"] = "%" + medicalRecordNo + "%"
            sqlCondition += " and pr.medical_record_no like :medicalRecordNo "

        state = request.args.get("state")  # 状态
        if state != None and state != "":
            filters["state"] = state
            sqlCondition += " and  d2.dict_value=:state "

        ecTime = request.args.get("ecTime")  # 取卵日期
        if ecTime != None and ecTime != "":
            ecTimeList = re.split("~", ecTime)
            filters["ecTimeStart"] = ecTimeList[0].strip() + " 00:00:00"  # 首尾去空格
            filters["ecTimeEnd"] = ecTimeList[1].strip() + " 23:59:59"  # 首尾去空格
            sqlCondition += " and  pr.ec_time >= :ecTimeStart "
            sqlCondition += " and  pr.ec_time <= :ecTimeEnd "

        insemiTime = request.args.get("insemiTime")  # 受精日期
        if insemiTime != None and insemiTime != "":
            insemiTimeList = re.split("~", insemiTime)
            filters["insemiTimeStart"] = (
                insemiTimeList[0].strip() + " 00:00:00"
            )  # 首尾去空格
            filters["insemiTimeEnd"] = insemiTimeList[1].strip() + " 23:59:59"  # 首尾去空格
            sqlCondition += " and  pr.insemi_time >= :insemiTimeStart "
            sqlCondition += " and  pr.insemi_time <= :insemiTimeEnd "

        # 查詢列表
        result = procedure_mapper.queryProcedureList(
            int(page), int(limit), sqlCondition, filters
        )
        procedureList = list(map(dict, result))
        if int(getFocus) == 1 and procedureList is not None:
            for i in range(len(procedureList)):
                procedureId = procedureList[i]["id"]
                dishCode = procedureList[i]["dishCode"].split(",")[0]
                focusPath = image_service.getImageFouce(procedureId, dishCode)
                procedureList[i]["focusPath"] = focusPath

        # 查询总数
        count = procedure_mapper.queryProcedureCount(sqlCondition, filters)
        restResult = RestResult(0, "OK", count, procedureList)
        return 200, jsonify(restResult.__dict__)
    except:
        return 400, "查询病历列表时发生错误!"


def getProcedureDetail(id):
    try:
        restResult = RestResult(0, "查无该病历详情!", 0, None)

        result = procedure_mapper.getProcedureById(id)
        if not result:
            return jsonify(restResult.__dict__)

        ec_time = None
        insemi_time = None

        if result.ec_time and result.ec_time != "0000-00-00 00:00:00":
            ec_time = parse_date(str(result.ec_time), 1)
        if result.insemi_time != "0000-00-00 00:00:00":
            insemi_time = parse_date(str(result.insemi_time), 1)

        result = dict(result)
        result["ec_time"] = ec_time
        result["insemi_time"] = insemi_time

        if result:
            restResult = RestResult(0, "OK", 1, result)

        return 200, jsonify(restResult.__dict__)
    except:
        return 400, "查询病历详情时时发生错误!"


def updateProcedure(request):
    id = request.form.get("id")
    patient_id = request.form.get("patientId")
    mobile = request.form.get("mobile")
    email = request.form.get("email")
    memo = request.form.get("memo")
    try:
        procedure_mapper.update(id, memo)
        patient_mapper.update(patient_id, mobile, email)

        # 读取上传云端代码块开关
        switch = conf["CLOUD_CODE_SWITCH"]
        if switch:
            # 同步患者信息,病例信息到云端
            import json
            from common import request_post

            url = conf["PATIENT_INFO_UPDATE_URL"]

            data = {
                "procedureId": id,
                "patientId": patient_id,
                "mobile": mobile,
                "email": email,
                "memo": memo,
            }

            request_post(url, json.dumps(data, ensure_ascii=False))

        return 200, "修改病历详情成功!"
    except:
        return 500, "修改病历详情时发生错误!"


def memo(request):
    id = request.args.get("procedureId")
    memo = request.args.get("memo")
    try:
        procedure_mapper.update(id, memo)
        return 200, "修改病历详情成功!"
    except:
        return 500, "修改病历详情时发生错误!"


def queryMedicalRecordNoList(request):
    # 动态组装查询条件
    sqlCondition = " where del_flag=0 "  # 动态sql
    filters = {}  # 动态参数
    limit = request.args.get("limit")  # 查询多少条
    query = request.args.get("query")  # 当前输入值
    if query != None and query != "":
        filters["query"] = "%" + query + "%"
        sqlCondition += " and medical_record_no like :query "

    sqlCondition += " limit " + limit
    result = procedure_mapper.queryMedicalRecordNoList(sqlCondition, filters)
    procedureList = list(map(dict, result))
    return jsonify(procedureList)


def queryMedicalRecordNoAndNameList(request):
    # 动态组装查询条件
    sqlCondition = " where del_flag=0 "  # 动态sql
    filters = {}  # 动态参数
    limit = request.args.get("limit")  # 查询多少条
    query = request.args.get("query")  # 当前输入值
    if query != None and query != "":
        filters["query"] = "%" + query + "%"
        sqlCondition += " and a.label like :query "

    sqlCondition += " limit " + limit
    result = procedure_mapper.queryMedicalRecordNoAndNameList(sqlCondition, filters)
    procedureList = list(map(dict, result))
    return jsonify(procedureList)


# 删除病历
def deleteProcedure(id):
    try:
        params = {"id": id, "delFlag": 1}
        procedure_mapper.deleteProcedure(params)
        return 200, "删除病例成功"
    except:
        return 500, "删除病例失败"


def queryProcedureViewList(request):
    try:
        medicalRecordNo = request.args.get("medicalRecordNo")
        if medicalRecordNo == None:
            return 400, "病历号不能为空!"

        # 查询字典表里程碑的节点
        result = dict_dao.queryDictListByClass("milestone")
        dictList = list(map(lambda x: x.to_dict(), result))

        # 查询字典表的胚胎结局
        result = dict_dao.queryDictListByClass("embryo_fate_type")
        embryoFateList = list(map(lambda x: x.to_dict(), result))

        procedureViewList = []
        # 表格的动态头
        tableObj = OrderedDict()
        tableObj["codeIndex"] = "箱皿胚胎"
        for key in dictList:
            tableObj[key["dictValue"]] = key["dictValue"] + "时间"
        tableObj["score"] = "评分"
        tableObj["embryoFate"] = "结局"
        procedureViewList.append(tableObj)
        # 查詢列表
        procedureList = procedure_mapper.queryProcedureViewList(medicalRecordNo)

        # 循环查询出来的值
        for key in procedureList:
            tableObj = OrderedDict()
            tableObj["codeIndex"] = key["codeIndex"]
            # 如果里程碑字段不为空
            if key["lcb"] != None:
                # 由于使用mysql GROUP_CONCAT函数 行转列 需要截取
                lcbstr = key["lcb"].split(",")
                for dictObj in dictList:
                    value = ""
                    for lcbjd in lcbstr:
                        lcb = lcbjd.split("#")
                        if dictObj["dictValue"] == lcb[0]:  # 如果相等的话
                            hour, minute = serie_to_time(lcb[2])
                            value = lcb[1] + "," + f"{hour:02d}H{minute:02d}M"
                            break
                    tableObj[dictObj["dictValue"]] = value
            else:
                for dictObj in dictList:
                    tableObj[dictObj["dictValue"]] = ""
            tableObj["score"] = key["score"]
            tableObj["embryoFate"] = key["embryoFate"]
            procedureViewList.append(tableObj)

        # 根据病历号查询患者信息
        patientRes = procedure_mapper.getPatientByMedicalRecordNo(medicalRecordNo)
        if patientRes != None:
            patient = dict(patientRes)
            for embryoFate in embryoFateList:
                count = procedure_mapper.getEmbryoFateCount(
                    medicalRecordNo, embryoFate["dictKey"]
                )
                patient[embryoFate["dictValue"]] = count

            resObj = OrderedDict()
            resObj["patient"] = patient
            resObj["procedureViewList"] = procedureViewList
            resObj["imageRoot"] = conf["EMBRYOAI_IMAGE_ROOT"]
            return 200, resObj
        else:
            return 200, None
    except:
        return 400, "查询周期综合视图列表时发生错误!"


def addProcedure(request):
    from common import uuid
    from entity.Patient import Patient

    id = uuid()
    patientName = request.form.get("patientName")
    if not patientName:
        return 400, "姓名不能为空!"
    idcardTypeId = 1  # 0-其他；1-身份证；2-社保；3-驾驶证；4-护照；5-港澳台通行证；6-回乡证
    idcardNo = request.form.get("nope")
    if not idcardNo:
        return 400, "身份证号码不能为空!"
    birthdate = request.form.get("birthdate")
    if not birthdate:
        return 400, "出生日期不能为空!"
    mobile = request.form.get("mobile")
    if not mobile:
        return 400, "移动电话不能为空!"
    insemiTypeId = request.form.get("aid")
    if not insemiTypeId:
        return 400, "授精方式不能为空!"
    insemiTime = request.form.get("insemi_time")
    if not insemiTime:
        return 400, "授精时间不能为空!"
    embryoNumber = request.form.get("embryo_number")
    if not embryoNumber:
        return 400, "胚胎个数不能为空!"
    embryoScoreId = request.form.get("embryo_score")
    if not embryoScoreId:
        return 400, "评分标准不能为空!"
    incubatorCode = request.form.get("incubator")
    if not incubatorCode:
        return 400, "采集目录不能为空!"
    dishCode = request.form.get("dish")
    if not dishCode:
        return 400, "采集目录不能为空!"
    catalog = request.form.get("catalogSelect")
    if not catalog:
        return 400, '采集目录不能为空!'
    catalog = catalog.split()[0]
    patientAge = request.form.get('patient_age')
    if not patientAge:
        return 400, "年龄不能为空!"
    medicalRecordNo = request.form.get("medical_record_no")
    if not medicalRecordNo:
        return 400, "病历号不能为空!"

    email = request.form.get("email")
    locationId = request.form.get("area")
    address = request.form.get("address")
    memo = request.form.get("memo")
    isDrinking = request.form.get("is_drinking")
    if isDrinking == "on":
        isDrinking = 1
    else:
        isDrinking = 0
    isSmoking = request.form.get("is_smoking")
    if isSmoking == "on":
        isSmoking = 1
    else:
        isSmoking = 0
    userId = request.form.get("userId")
    patientHeight = request.form.get("patient_height")
    if not patientHeight:
        patientHeight = None
    patientWeight = request.form.get("patient_weight")
    if not patientWeight:
        patientWeight = None
    ecTime = request.form.get("ec_time")
    if not ecTime:
        ecTime = None
    ecCount = request.form.get("ec_count")
    state = 1  # 病历已登记完善：2；结束采集：3；已回访：

    createTime = updateTime = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.localtime(time.time())
    )

    patient = Patient(
        id=id,
        idcardNo=idcardNo,
        idcardTypeId=idcardTypeId,
        patientName=patientName,
        birthdate=birthdate,
        country="中国",
        locationId=locationId,
        address=address,
        email=email,
        mobile=mobile,
        delFlag=0,
        createTime=createTime,
        updateTime=updateTime,
        isDrinking=isDrinking,
        isSmoking=isSmoking,
    )

    procedureId = uuid()
    procedure = Procedure(
        id=procedureId,
        patientId=id,
        userId=userId,
        patientAge=patientAge,
        patientHeight=patientHeight,
        patientWeight=patientWeight,
        ecTime=ecTime,
        ecCount=ecCount,
        insemiTime=insemiTime,
        insemiTypeId=insemiTypeId,
        state=state,
        delFlag=0,
        medicalRecordNo=medicalRecordNo,
        embryoScoreId=embryoScoreId,
        memo=memo,
    )

    # 保存病历表
    code, msg = procedure_mapper.save(
        procedure, patient, incubatorCode, dishCode, catalog, procedureId
    )
    if code == 500:
        return code, msg

    # 读取上传云端代码块开关
    switch = conf["CLOUD_CODE_SWITCH"]
    if switch:
        # 同步患者信息,病例信息到云端
        import json
        from common import request_post
        from entity.PatientInfo import PatientInfo
        from entity.PatientBaseInfo import PatientBaseInfo
        from entity.PatientCaseInfo import PatientCaseInfo

        url = conf["PATIENT_INFO_INSERT_URL"]

        patient_base_info = PatientBaseInfo(
            id=id,
            idcardNo=idcardNo,
            idcardTypeId=idcardTypeId,
            patientName=patientName,
            birthdate=birthdate,
            country="中国",
            locationId=locationId,
            address=address,
            email=email,
            mobile=mobile,
            delFlag=0,
            createTime=createTime,
            updateTime=updateTime,
            isDrinking=isDrinking,
            isSmoking=isSmoking,
        )

        # 获取机构注册ID
        import service.front.organization_service as org_service

        org_config = org_service.getOrganConfig()
        orgId = org_config["orgId"]

        patient_case_info = PatientCaseInfo(
            id=procedureId,
            orgId=orgId,
            patientId=id,
            userId=userId,
            patientAge=patientAge,
            patientHeight=patientHeight,
            patientWeight=patientWeight,
            ecTime=ecTime,
            ecCount=ecCount,
            insemiTime=insemiTime,
            insemiTypeId=insemiTypeId,
            state=state,
            delFlag=0,
            medicalRecordNo=medicalRecordNo,
            embryoScoreId=embryoScoreId,
            memo=memo,
        )
        patientInfo = PatientInfo(
            patient_base_info.__dict__, patient_case_info.__dict__
        )
        request_post(url, json.dumps(patientInfo.__dict__, ensure_ascii=False))

    return 200, "新增病历成功!"
