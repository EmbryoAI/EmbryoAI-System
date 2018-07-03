from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryProcedureList(page,limit,filters):
#     pagination = Procedure.query.filter_by(**filters).order_by(Procedure.insemiTime.desc()).paginate(page,per_page=limit,error_out=False)
#     pagination = Procedure.query.filter_by(**filters).paginate(page,per_page=limit,error_out=False)
    sql = text("""
        SELECT pr.id as id,medical_record_no AS medical_record_no,pa.patient_name AS patient_name,
        pr.patient_age AS patient_age,COUNT(DISTINCT e.id) AS pts,
        CONCAT(pr.insemi_time) AS insemi_time,d.dict_value AS sjfs, CONCAT('D',DATEDIFF(NOW(),pr.insemi_time)) AS zzjd,d2.dict_value AS state,
        GROUP_CONCAT(DISTINCT po.dish_id) xst 
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
        GROUP BY pr.id 
        """)
    print(sql)
    
    # 执行sql得出结果
    result = db.session.execute(sql) 
    sql_result = result.fetchall()
  
    return sql_result



def queryProcedureCount(filters):
#     pagination = Procedure.query.filter_by(**filters).order_by(Procedure.insemiTime.desc()).paginate(page,per_page=limit,error_out=False)
#     pagination = Procedure.query.filter_by(**filters).paginate(page,per_page=limit,error_out=False)
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
        """)
    print(count_sql)
    # 计算总条数
    count_result = db.session.execute(count_sql)
    total_size = count_result.fetchone()[0]
 
    return total_size

def getProcedureById(procedureID):
    sql = text("""
        SELECT pro.`id`,pat.`patient_name`, pat.`idcard_no`,pat.`birthdate`,
        pat.`email`, pat.`mobile`,pat.`address`,pat.`is_smoking`,pat.`is_drinking`, 
        pro.`patient_age`, pro.`patient_height`,pro.`patient_weight`,pro.`ec_time`, 
        pro.`insemi_time`,pro.`memo`,COUNT(DISTINCT e.id) AS embryo_num,d.dict_value AS insemi_type 
        FROM t_patient pat LEFT JOIN t_procedure pro ON pat.`id` = pro.`patient_id` LEFT JOIN 
        t_embryo e ON pro.id=e.procedure_id LEFT JOIN sys_dict d ON pro.insemi_type_id=d.dict_key 
        AND d.dict_class='insemi_type' WHERE pro.`id` = :procedureID GROUP BY pro.id
        """)
    print(sql)
    return db.session.execute(sql, {'procedureID':procedureID}).fetchone()

def update(id, mobile, email):
    try:
        sql = text("UPDATE `t_patient` SET mobile = :mobile, email = :email WHERE id = :id")
        print(sql)
        db.session.execute(sql,{'id':id, 'mobile':mobile, 'email':email})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("修改病历信息时发生错误",e.message,e)