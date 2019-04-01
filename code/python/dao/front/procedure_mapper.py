from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc


def queryProcedureList(page,limit,sqlCondition,filters):
#     pagination = Procedure.query.filter_by(**filters).order_by(Procedure.insemiTime.desc()).paginate(page,per_page=limit,error_out=False)
#     pagination = Procedure.query.filter_by(**filters).paginate(page,per_page=limit,error_out=False)
    try:
        sql = text("""
            SELECT pr.id as id,medical_record_no AS medical_record_no,pa.patient_name AS patient_name,
            pr.patient_age AS patient_age,COUNT(DISTINCT e.id) AS pts,
            CONCAT(pr.insemi_time) AS insemi_time,d.dict_value AS sjfs,CONCAT('D',DATEDIFF(IF(pr.cap_end_time,pr.cap_end_time,NOW()),pr.insemi_time)) AS zzjd ,d2.dict_value AS state,
            GROUP_CONCAT(DISTINCT po.dish_id) xst ,GROUP_CONCAT(DISTINCT sd.dish_code) dishCode,si.incubator_code incubatorCode
            FROM t_procedure pr 
            LEFT JOIN  t_patient pa 
            ON pr.patient_id=pa.id 
            LEFT JOIN t_embryo e 
            ON pr.id=e.procedure_id 
            LEFT JOIN t_procedure_dish po 
            ON pr.id=po.procedure_id 
            LEFT JOIN sys_dict d 
            ON pr.insemi_type_id=d.dict_key AND d.dict_class='insemi_type' 
            LEFT JOIN sys_dict d2 
            ON pr.state=d2.dict_key AND d2.dict_class='state'  
            LEFT JOIN sys_dish sd ON po.dish_id = sd.id
            LEFT JOIN sys_incubator si ON sd.incubator_id = si.id
            """+sqlCondition+"""
            GROUP BY pr.id 
            ORDER BY pr.insemi_time DESC
            limit :index,:limit
            """)
        print(sql)
        index = 0
        if page > 1 :
            index = (page - 1) * limit
        filters["index"] = index
        filters["limit"] = limit        
        # 执行sql得出结果
        result = db.session.execute(sql,filters) 
        sql_result = result.fetchall()
      
        return sql_result
    except Exception as e:
        print_exc();
        raise DatabaseError("获取病历列表异常!",e.message,e)
        return None
    finally:
        db.session.remove()



def queryProcedureCount(sqlCondition,filters):
#     pagination = Procedure.query.filter_by(**filters).order_by(Procedure.insemiTime.desc()).paginate(page,per_page=limit,error_out=False)
#     pagination = Procedure.query.filter_by(**filters).paginate(page,per_page=limit,error_out=False)
    try:
        count_sql = text("""
            SELECT  COUNT(DISTINCT pr.id) as count 
            FROM t_procedure pr 
            LEFT JOIN  t_patient pa 
            ON pr.patient_id=pa.id 
            LEFT JOIN t_embryo e 
            ON pr.id=e.procedure_id 
            LEFT JOIN t_procedure_dish po 
            ON pr.id=po.procedure_id 
            LEFT JOIN sys_dict d 
            ON pr.insemi_type_id=d.dict_key AND d.dict_class='insemi_type' 
            LEFT JOIN sys_dict d2 
            ON pr.state=d2.dict_key AND d2.dict_class='state'
            """+sqlCondition+"""
            """)
        print(count_sql)
        # 计算总条数
        count_result = db.session.execute(count_sql,filters)
        total_size = count_result.fetchone()[0]
     
        return total_size
    except Exception as e:
        print_exc();
        raise DatabaseError("获取病历总数异常!",e.message,e)
        return None
    finally:
        db.session.remove()

def getProcedureById(procedureID):
    try:
        sql = text("""
            SELECT pro.`id`,pat.`patient_name`, pat.`idcard_no`,
                        DATE_FORMAT(pat.`birthdate`,'%Y-%m-%d') AS birthdate,
                        pat.`email`, pat.`mobile`,pat.`address`,sl.`sole_name`,pat.`country`, 
                        pat.`is_smoking`,pat.`is_drinking`, pro.`patient_age`, pro.`patient_height`,
                        pro.`patient_weight`,pro.`ec_time` AS ec_time,pro.`ec_count` AS ec_count, 
                        pro.`insemi_time` AS insemi_time,pro.`memo`,pro.`medical_record_no` AS medical_record_no, 
                        COUNT(DISTINCT e.id) AS embryo_num,d.dict_value AS insemi_type,
                        CONCAT('D',DATEDIFF(IF(pro.cap_end_time,pro.cap_end_time,NOW()),pro.insemi_time)) AS zzjd,
                        tr.`rule_name` AS rule_name, pat.`id` AS patient_id   
            FROM t_patient pat 
            LEFT JOIN t_procedure pro 
            ON pat.`id` = pro.`patient_id` 
            LEFT JOIN t_embryo e 
            ON pro.id=e.procedure_id 
            LEFT JOIN sys_dict d 
            ON pro.insemi_type_id=d.dict_key 
            AND d.dict_class='insemi_type' 
            LEFT JOIN `sys_location` sl 
            ON pat.`location_id` = sl.`id` 
            JOIN `t_rule` tr 
            ON pro.`embryo_score_id` = tr.`id` 
            WHERE pro.`id` = :procedureID GROUP BY pro.id
            """)
        return db.session.execute(sql, {'procedureID':procedureID}).fetchone()
    except Exception as e:
        raise DatabaseError("根据ID查询病历时发生错误",e.message,e)
        return None
    finally:
        db.session.remove()

def update(id, memo):
    try:
        sql = text("UPDATE `t_procedure` SET memo = :memo WHERE id = :id")
        print(sql)
        db.session.execute(sql,{'id':id, 'memo':memo})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改病历信息时发生错误",e.message,e)
    finally:
        db.session.remove()
    
def queryMedicalRecordNoList(sqlCondition,filters):
    try:
        sql = text("""
           SELECT medical_record_no AS 'value',medical_record_no AS label FROM  t_procedure
        """+sqlCondition)
        print(sql)
    
        # 执行sql得出结果
        result = db.session.execute(sql,filters) 
        sql_result = result.fetchall()
        return sql_result
    except Exception as e:
        raise DatabaseError("查询病历号时发生错误",e.message,e)
        return None
    finally:
        db.session.remove()


def queryMedicalRecordNoAndNameList(sqlCondition,filters):
    try:
        sql = text("""
            SELECT * FROM (
             SELECT medical_record_no AS 'value',medical_record_no AS label FROM  t_procedure
             UNION ALL 
             SELECT patient_name AS 'value',patient_name AS label FROM  t_patient
            ) a
        """+sqlCondition)
        print(sql)
    
        # 执行sql得出结果
        result = db.session.execute(sql,filters) 
        sql_result = result.fetchall()
        return sql_result
    except Exception as e:
        raise DatabaseError("查询病历号时发生错误",e.message,e)
        return None
    finally:
        db.session.remove()

#删除病历异常
def deleteProcedure(params):
    try :
        sql = text('update t_procedure set del_flag=:delFlag '
            'where id=:id')
        print(sql)
        db.session.execute(sql, params)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('删除病历时异常', e.message, e)
    finally:
        db.session.remove()

#根据主键ID查询
def getProcedure(id):
    try :
        return db.session.query(Procedure).filter(Procedure.id == id).one_or_none()
    except Exception as e:
        raise DatabaseError('根据主键ID查询病历时异常', e.message, e)
        return None
    finally:
        db.session.remove()
        
#根据病历号查询周期下朋友胚胎的里程碑  -  周期综合视图
def queryProcedureViewList(medicalRecordNo):
    try:
        sql = text("""
        SELECT CONCAT(i.incubator_code,'-',d.dish_code,'-',e.embryo_index) AS codeIndex, 
            GROUP_CONCAT(dict1.dict_value,"#",m.thumbnail_path,"#",m.milestone_time ORDER BY m.milestone_time) lcb,
            e.embryo_score AS score ,dict2.dict_value AS embryoFate
            FROM t_embryo e
            LEFT JOIN t_procedure t
            ON e.procedure_id = t.id
            LEFT JOIN  t_patient pa 
            ON t.patient_id=pa.id 
            LEFT JOIN t_milestone m
            ON m.embryo_id = e.id
            LEFT JOIN t_procedure_dish td
            ON t.id=td.procedure_id
            LEFT JOIN sys_dish d
            ON td.dish_id=d.id
            LEFT JOIN sys_incubator i
            ON d.incubator_id = i.id
        LEFT JOIN sys_dict dict1
        ON m.milestone_id = dict1.dict_key AND dict1.dict_class='milestone' 
        LEFT JOIN sys_dict dict2
        ON e.embryo_fate_id = dict2.dict_key AND dict2.dict_class='embryo_fate_type' 
            WHERE  t.id = (SELECT id FROM t_procedure WHERE medical_record_no=:medicalRecordNo ORDER BY  id  LIMIT 1 )  
            GROUP BY e.id       
        """)
        return db.session.execute(sql, {'medicalRecordNo':medicalRecordNo}).fetchall()
    except Exception as e:
        raise DatabaseError('根据主键ID查询病历时异常', e.message, e)
        return None
    finally:
        db.session.remove()


#根据病历号查询患者信息  -  周期综合视图
def getPatientByMedicalRecordNo(medicalRecordNo):
    try:
        sql = text("""
            SELECT
              p.patient_name AS patientName,
              t.patient_age AS patientAge,
              CONCAT(t.insemi_time) AS insemiTime,
              COUNT(e.id) AS '胚胎总数'
            FROM t_procedure t
              LEFT JOIN t_patient p
                ON t.patient_id = p.id
              LEFT JOIN  t_embryo e
               ON e.procedure_id = t.id
            WHERE  t.medical_record_no = :medicalRecordNo 
            GROUP BY t.id ORDER BY  t.id  LIMIT 1
        """)
        return db.session.execute(sql, {'medicalRecordNo':medicalRecordNo}).fetchone()
    except Exception as e:
        raise DatabaseError('根据根据病历号查询患者信息异常', e.message, e)
        return None
    finally:
        db.session.remove()

#根据病历号和胚胎结局查询对应的结局数  -  周期综合视图
def getEmbryoFateCount(medicalRecordNo,embryoFateId):
    try:
        sql = text("""
            SELECT
              COUNT(e.id) pts
            FROM t_procedure t
                LEFT JOIN  t_patient pa 
            ON t.patient_id=pa.id 
              LEFT JOIN t_embryo e
                ON e.procedure_id = t.id
            WHERE  t.medical_record_no = :medicalRecordNo  AND e.embryo_fate_id=:embryoFateId
        """)
        return db.session.execute(sql, {'medicalRecordNo':medicalRecordNo,'embryoFateId':embryoFateId}).fetchone()[0]
    except Exception as e:
        raise DatabaseError('根据主键ID查询病历时异常', e.message, e)
        return None
    finally:
        db.session.remove()


def save(procedure, patient, incubatorCode, dishCode, catalog, procedureId):
    import dao.front.patient_mapper as patient_mapper
    import dao.front.incubator_mapper as incubator_mapper
    from common import uuid
    from entity.Incubator import Incubator
    import time
    import dao.front.dish_mapper as dish_mapper
    from entity.Dish import Dish
    import dao.front.procedure_dish_mapper as procedure_dish_mapper
    
    from entity.ProcedureDish import ProcedureDish
    import json,os
    from app import conf
    from task.ini_parser import EmbryoIniParser as parser
    import dao.front.cell_mapper as cell_mapper
    from entity.Cell import Cell
    from entity.Embryo import Embryo
    import dao.front.embryo_mapper as embryo_mapper
    try :
        #保存周期数据
        db.session.add(procedure)
        #保存患者信息表
        db.session.add(patient)
        #先查询是否存在培养箱,如果没有则新增
        createTime = updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())) 
        incubator = db.session.query(Incubator).filter(Incubator.incubatorCode == incubatorCode).one_or_none()
        if not incubator:
            incubatorId = uuid()
            incubator = Incubator(id=incubatorId, incubatorCode=incubatorCode, createTime=createTime, updateTime=updateTime, delFlag=0)
            db.session.add(incubator)
        else:
            incubatorId = incubator.id 
        #先查询是否存在培养皿,如果没有则新增
        dishCodeList = dishCode.split(',')
        for dish_code in dishCodeList:
            code = dish_code[-1]
            dish = db.session.query(Dish).filter(Dish.incubatorId == incubatorId, Dish.dishCode == code).one_or_none()
            if not dish:
                dishId = uuid()
                dish = Dish(id=dishId, incubatorId=incubator.id, dishCode=code, createTime=createTime, updateTime=updateTime)
                db.session.add(dish)
            else:
                dishId = dish.id 
            #保存周期与皿与采集目录关联表
            procedureDishId = uuid()
            pd = ProcedureDish(id=procedureDishId, procedureId=procedure.id, dishId=dishId, imagePath=catalog)
            db.session.add(pd)

            ini_path = conf['EMBRYOAI_IMAGE_ROOT'] + os.path.sep + catalog + os.path.sep + 'DishInfo.ini'
            config = parser(ini_path)
            dishes = [f'Dish{code}Info']
            wells = [f'Well{i}Avail' for i in range(1, 13)]
            embryos = [index for d in dishes for index,w in enumerate(wells) if config[d][w]=='1']
            print('embryos:',embryos)
            #孔表新增记录
            for i in embryos:
                cellCode = i+1
                print('cellCode:',cellCode)
                cell = db.session.query(Cell).filter(Cell.dishId == dishId,Cell.cellCode == cellCode).one_or_none()
                if not cell:
                    cellId = uuid()
                    cell = Cell(id=cellId, dishId=dishId, cellCode=cellCode, createTime=createTime, updateTime=updateTime)
                    db.session.add(cell)
                else:
                    cellId = cell.id

                #胚胎表新增记录
                embryoId = uuid()
                embryo = Embryo(id=embryoId, embryoIndex=i+1, procedureId=procedure.id, cellId=cellId)
                db.session.add(embryo)

        db.session.commit()
        return 200, '新增病历成功!'
    except Exception as e:
        print('新增病历失败:', e)
        db.session.rollback()
        print_exc()
        return 500, '新增病历失败!'
    finally:
        db.session.remove()

#查询所有采集结束时间为空的数据
def queryCollectList():
    try:
        sql = text("""
            SELECT t.id AS procedureId,td.dish_id AS dishId,td.image_path AS imagePath  
            FROM t_procedure t
            LEFT JOIN t_procedure_dish td
            ON t.id = td.procedure_id
            WHERE t.cap_end_time IS NULL 
        """)
        return db.session.execute(sql).fetchall()
    except Exception as e:
        raise DatabaseError('查询所有采集结束时间为空的数据时发生错误', e.message, e)
        return None
    finally:
        db.session.remove()

#根据周期ID修改 采集开始时间 和 采集结束时间
def updateCollect(procedureId,capStartTime,capEndtime):
    try :
        sql = text("""
            UPDATE t_procedure 
            SET
            cap_start_time =:capStartTime, 
            cap_end_time =:capEndtime
            WHERE id =:procedureId
        """)
        db.session.execute(sql,{'capStartTime':capStartTime,'capEndtime':capEndtime,'procedureId':procedureId})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('设置里程碑时发生错误!', e.message, e)
    finally:
        db.session.remove()