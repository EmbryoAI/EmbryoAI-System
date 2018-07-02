from app import db
from entity.Procedure import Procedure
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryProcedureList(page,limit,filters):
#     pagination = Procedure.query.filter_by(**filters).order_by(Procedure.insemiTime.desc()).paginate(page,per_page=limit,error_out=False)
    pagination = Procedure.query.filter_by(**filters).paginate(page,per_page=limit,error_out=False)
#     sql = text("update sys_incubator set incubator_code=:incubatorCode,incubator_brand=:incubatorBrand, incubator_type=:incubatorType"
#         ', incubator_description=:incubatorDescription '
#         ', update_time=:updateTime '
#             'where id=:id')
#         print(sql)
#         db.session.execute(sql, params)
#         
        
        

# pr.patient_age as '年龄',count(DISTINCT e.id) as '胚胎数',
# pr.insemi_time as '授精时间',d.dict_value as '授精方式','不知道查哪' as '最终阶段',d2.dict_value as '状态',
# group_concat(DISTINCT po.id) '皿视图'
# from t_procedure pr
# left join  t_patient pa
# on pr.patient_id=pa.id
# left join t_embryo e
# on pr.id=e.procedure_id
# left join t_procedure_dish po
# on pr.id=po.procedure_id
# left join sys_dict d
# on pr.insemi_type_id=d.dict_key and d.dict_class='insemi_type'
# LEFT JOIN sys_dict d2
# ON pr.state=d2.dict_key AND d2.dict_class='state'


    return pagination

def getProcedureById(procedureID):
    try :
        sql = text("SELECT pro.`id`,pat.`patient_name`, pat.`idcard_no`,pat.`birthdate`,"
        "pat.`email`, pat.`mobile`,pat.`address`,pat.`is_smoking`,pat.`is_drinking`, "
        "pro.`patient_age`, pro.`patient_height`,pro.`patient_weight`,pro.`ec_time`, "
        "pro.`insemi_time`,pro.`memo`,COUNT(DISTINCT e.id) AS embryoNum,d.dict_value AS insemi_type "
        "FROM t_patient pat LEFT JOIN t_procedure pro ON pat.`id` = pro.`patient_id` LEFT JOIN "
        "t_embryo e ON pro.id=e.procedure_id LEFT JOIN sys_dict d ON pro.insemi_type_id=d.dict_key "
        "AND d.dict_class='insemi_type' WHERE pro.`id` = :procedureID")
        print(sql)
        return db.session.execute(sql, {'procedureID':procedureID})
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('查询病历详情数据时发生错误', e.message, e)