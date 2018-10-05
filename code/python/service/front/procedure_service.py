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
from task.TimeSeries import TimeSeries,serie_to_time
from collections import OrderedDict


def queryProcedureList(request):
    try:
        page = request.args.get('page')
        if page==None:
           page=1
        limit = request.args.get('limit')
        if limit==None:
            limit=10

        #动态组装查询条件
        sqlCondition = " where pr.del_flag=0 "#动态sql
        filters = {}#动态参数
        userName = request.args.get('userName')#用户名字
        if userName!=None and userName!="":
            filters['userName']="%"+userName+"%"
            sqlCondition += " and pa.patient_name like :userName "

        medicalRecordNo = request.args.get('medicalRecordNo')#病历号
        if medicalRecordNo!=None and medicalRecordNo!="":
            filters['medicalRecordNo']="%"+medicalRecordNo+"%"
            sqlCondition += " and pr.medical_record_no like :medicalRecordNo "

        state = request.args.get('state')#状态
        if state!=None and state!="":
            filters['state']=state
            sqlCondition += " and  d2.dict_value=:state "
            
        ecTime = request.args.get('ecTime')#取卵日期
        if ecTime!=None and ecTime!="":
            ecTimeList = re.split('~', ecTime)
            filters['ecTimeStart']=ecTimeList[0].strip()+" 00:00:00" #首尾去空格
            filters['ecTimeEnd']=ecTimeList[1].strip()+" 23:59:59" #首尾去空格
            sqlCondition += " and  pr.ec_time >= :ecTimeStart "
            sqlCondition += " and  pr.ec_time <= :ecTimeEnd "
        
        insemiTime = request.args.get('insemiTime')#受精日期
        if insemiTime!=None and insemiTime!="":
            insemiTimeList = re.split('~', insemiTime)
            filters['insemiTimeStart']=insemiTimeList[0].strip()+" 00:00:00" #首尾去空格
            filters['insemiTimeEnd']=insemiTimeList[1].strip()+" 23:59:59" #首尾去空格
            sqlCondition += " and  pr.insemi_time >= :insemiTimeStart "
            sqlCondition += " and  pr.insemi_time <= :insemiTimeEnd "
 
        #查詢列表
        result = procedure_mapper.queryProcedureList(int(page),int(limit),sqlCondition,filters)
        procedureList = list(map(dict, result))
        #查询总数
        count = procedure_mapper.queryProcedureCount(sqlCondition,filters)
        
    except:
        return 400, '查询病历列表时发生错误!'
    restResult = RestResult(0, "OK", count, procedureList)
    return jsonify(restResult.__dict__)

def getProcedureDetail(id):
    restResult = RestResult(0, "查无该病历详情!", 0, None)

    result = procedure_mapper.getProcedureById(id)
    if not result:
        return jsonify(restResult.__dict__)

    ec_time = None
    insemi_time = None

    if result.ec_time and result.ec_time != '0000-00-00 00:00:00':
        ec_time = parse_date(str(result.ec_time), 1)
    if result.insemi_time != '0000-00-00 00:00:00':
        insemi_time = parse_date(str(result.insemi_time), 1)

    result = dict(result)
    result['ec_time'] = ec_time
    result['insemi_time'] = insemi_time
    

    if result:
        restResult = RestResult(0, "OK", 1, result)
    
    return jsonify(restResult.__dict__)

def updateProcedure(request):
    id = request.form.get('id')
    mobile = request.form.get('mobile')
    email = request.form.get('email')
    memo = request.form.get('memo')
    try:
        procedure_mapper.update(id, memo)
        patient_mapper.update(id, mobile, email)
    except:
        return 500, '修改病历详情时发生错误!'
    return 200, '修改病历详情成功!'

def memo(request):
    id = request.args.get('procedureId')
    memo = request.args.get('memo')
    try:
        procedure_mapper.update(id, memo)
    except:
        return 500, '修改病历详情时发生错误!'
    return 200, '修改病历详情成功!'

def queryMedicalRecordNoList(request):
        #动态组装查询条件
       sqlCondition = " where 1=1 " #动态sql
       filters = {}#动态参数
       limit = request.args.get('limit')#查询多少条
       query = request.args.get('query')#当前输入值
       if query!=None and query!="":
           filters['query']="%"+query+"%"
           sqlCondition += " and medical_record_no like :query "
           
       sqlCondition += " limit "+limit
       result = procedure_mapper.queryMedicalRecordNoList(sqlCondition,filters)
       procedureList = list(map(dict, result))
       return jsonify(procedureList)
   
#删除病历
def deleteProcedure(id):
    try:
        params = {'id': id, 'delFlag': 1}
        procedure_mapper.deleteProcedure(params)
    except:
        return 400, {'msg': '删除病历时发生错误'}
    return 204, None


def queryProcedureViewList(request):
    try:
        medicalRecordNo = request.args.get('medicalRecordNo')
        if medicalRecordNo==None:
            return 400, '病历号不能为空!'
        
        #查询字典表里程碑的节点
        result = dict_dao.queryDictListByClass("milestone")
        dictList = list(map(lambda x: x.to_dict(),result))
        
        #查询字典表的胚胎结局
        result = dict_dao.queryDictListByClass("embryo_fate_type")
        embryoFateList = list(map(lambda x: x.to_dict(),result))
        
        procedureViewList=[]
        #表格的动态头
        tableObj=OrderedDict()
        tableObj["codeIndex"] = "箱皿胚胎"
        for key in dictList:
            tableObj[key['dictValue']] = key['dictValue']
        tableObj["score"] = "评分"
        tableObj["embryoFate"] = "结局"
        procedureViewList.append(tableObj)
        #查詢列表
        procedureList = procedure_mapper.queryProcedureViewList(medicalRecordNo)
     
        #循环查询出来的值
        for key in procedureList:
            tableObj=OrderedDict()
            tableObj["codeIndex"] = key["codeIndex"]
            #如果里程碑字段不为空
            if key['lcb']!=None:
                #由于使用mysql GROUP_CONCAT函数 行转列 需要截取
                lcbstr = key['lcb'].split(",")
                for dictObj in dictList:
                    value = ""
                    for lcbjd in lcbstr:
                        lcb = lcbjd.split("#")
                        if dictObj['dictValue'] == lcb[0]: #如果相等的话
                            hour, minute = serie_to_time(lcb[2])
                            value = lcb[1]+","+ f'{hour:02d}H{minute:02d}M'
                            break
                    tableObj[dictObj['dictValue']] = value
            else:
                for dictObj in dictList:
                    tableObj[dictObj['dictValue']] = ""
            tableObj["score"] = key["score"]
            tableObj["embryoFate"] = key["embryoFate"]
            procedureViewList.append(tableObj)
            
        #根据病历号查询患者信息
        patientRes = procedure_mapper.getPatientByMedicalRecordNo(medicalRecordNo)
        if patientRes!=None:
            patient = dict(patientRes)
            for embryoFate in embryoFateList:
                count = procedure_mapper.getEmbryoFateCount(medicalRecordNo,embryoFate['dictKey'])
                patient[embryoFate['dictValue']] = count
            
            resObj=OrderedDict()
            resObj["patient"] = patient
            resObj["procedureViewList"] = procedureViewList
                
            return 200,resObj
        else:
            return 200,None
    except:
        return 400, '查询周期综合视图列表时发生错误!'
    
def addProcedure(request):
    from common import uuid
    from entity.Patient import Patient
    from entity.Incubator import Incubator
    from entity.Dish import Dish
    from entity.Cell import Cell
    from entity.ProcedureDish import ProcedureDish
    import dao.front.incubator_mapper as incubator_mapper
    import dao.front.dish_mapper as dish_mapper
    import dao.front.procedure_dish_mapper as procedure_dish_mapper
    from entity.Embryo import Embryo
    import dao.front.embryo_mapper as embryo_mapper
    import dao.front.cell_mapper as cell_mapper

    id = uuid()
    patientName = request.form.get('patientName')
    if not patientName:
        return 400, '姓名不能为空!'
    idcardTypeId = 1 #0-其他；1-身份证；2-社保；3-驾驶证；4-护照；5-港澳台通行证；6-回乡证
    idcardNo = request.form.get('nope')
    if not idcardNo:
        return 400, '身份证号码不能为空!'
    birthdate = request.form.get('birthdate')
    if not birthdate:
        return 400, '出生日期不能为空!'
    mobile = request.form.get('mobile')
    if not mobile:
        return 400, '移动电话不能为空!'
    insemiTypeId = request.form.get('aid')
    if not insemiTypeId:
        return 400, '授精方式不能为空!'
    insemiTime = request.form.get('insemi_time')
    if not insemiTime:
        return 400, '授精时间不能为空!'
    embryoNumber = request.form.get('embryo_number')
    if not embryoNumber:
        return 400, '胚胎个数不能为空!'
    embryoScore = request.form.get('embryo_score')
    if not embryoScore:
        return 400, '评分标准不能为空!'
    incubatorCode = request.form.get('incubator')
    if not incubatorCode:
        return 400, '培养箱不能为空!'
    dishCode = request.form.get('dish')
    if not dishCode:
        return 400, '培养皿不能为空!'
    patientAge = request.form.get('patient_age')
    if not patientAge:
        return 400, '年龄不能为空!'
    medicalRecordNo = request.form.get('medical_record_no')
    if not medicalRecordNo:
        return 400, '病历号不能为空!'
    email = request.form.get('email')
    locationId = request.form.get('area')
    address = request.form.get('address')
    isDrinking = request.form.get('is_drinking')
    isSmoking = request.form.get('is_smoking')
    userId = request.form.get('userId')
    patientHeight = request.form.get('patient_height')
    if not patientHeight:
        patientHeight = None
    patientWeight = request.form.get('patient_weight')
    if not patientWeight:
        patientWeight = None
    ecTime = request.form.get('ec_time')
    if not ecTime:
        ecTime = None
    ecCount = request.form.get('ec_count')
    well_id = request.form.get('well_id')
    state = 1 #病历已登记完善：2；结束采集：3；已回访：

    createTime = updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 

    patient = Patient(id=id, idcardNo=idcardNo, idcardTypeId=idcardTypeId, patientName=patientName,
                    birthdate=birthdate, country='中国', locationId=locationId, address=address,
                    email=email, mobile=mobile, delFlag=0, createTime=createTime, updateTime=updateTime,
                    isDrinking=isDrinking, isSmoking=isSmoking)

    procedureId = uuid()
    procedure = Procedure(id=procedureId, patientId=id, userId=userId, patientAge=patientAge,
                    patientHeight=patientHeight, patientWeight=patientWeight, ecTime=ecTime,
                    ecCount=ecCount, insemiTime=insemiTime, insemiTypeId=insemiTypeId, state=state,
                    delFlag=0, medicalRecordNo=medicalRecordNo)
    

    try:
        #保存患者信息表
        patient_mapper.save(patient)
        #保存病历表
        procedure_mapper.save(procedure)
        #先查询是否存在培养箱,如果没有则新增
        incubator = incubator_mapper.getByIncubatorCode(incubatorCode)
        if not incubator:
            incubatorId = uuid()
            incubator = Incubator(id=incubatorId, incubatorCode=incubatorCode, createTime=createTime,
                    updateTime=updateTime, delFlag=0)
            incubator_mapper.save(incubator)
        #先查询是否存在培养名,如果没有则新增
        dishCodeList = dishCode.split('|')
        for dish_code in dishCodeList:
            dish_code = dish_code.split(',')
            for i in range(0, len(dish_code), 2):
                imagePath = dish_code[i+1]
                code = dish_code[i][-1]
                dish = dish_mapper.getByDishCode(code)
                if not dish:
                    dishId = uuid()
                    dish = Dish(id=dishId, incubatorId=incubator.id, dishCode=code, createTime=createTime,
                                updateTime=updateTime)
                    dish_mapper.save(dish)
                pd = procedure_dish_mapper.queryByProcedureIdAndDishId(procedureId, code)
                if not pd:
                    procedureDishId = uuid()
                    pd = ProcedureDish(id=procedureDishId, procedureId=procedureId, dishId=dishId,
                                    imagePath=imagePath)
                    procedure_dish_mapper.save(pd)
        
        well_id = well_id.split(',')
        #孔表新增记录
        for i in well_id:
            cellId = uuid()
            cell = Cell(id=cellId, dishId=dishId, cellCode=i, createTime=createTime, updateTime=updateTime)
            cell_mapper.save(cell)
            #胚胎表新增记录
            embryoId = uuid()
            embryo = Embryo(id=embryoId, embryoIndex=i, procedureId=procedureId, cellId=cellId, embryoFateId=4)
            embryo_mapper.save(embryo)

    except:
        return 500, '新增病历失败!'

    return 200, '新增病历成功!'
