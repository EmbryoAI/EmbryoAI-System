from app import db
from entity.Dish import Dish
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def queryById(dishId):
    try:
        dish =  db.session.query(Dish).filter(Dish.id == dishId).one_or_none()
    except Exception as e:
        return dish
    finally:
        db.session.close()
    return dish

def findDishByIncubatorId(params):
    sql = text("""
        SELECT sd.id AS dishId,sd.dish_code AS dishCode, COUNT(DISTINCT te.cell_id) AS embryoCount,tp.id procedureId,
        p.patient_name name,tp.patient_age age, CONCAT(tp.insemi_time) insemiTime,tpd.image_path imagePath,dict.dict_value insemiType, 
        CONCAT('D', DATEDIFF(IF(tp.cap_end_time,tp.cap_end_time, NOW()),tp.insemi_time)) AS stage, IFNULL(a.embryoSum,0) embryoSum
        FROM sys_dish sd
        LEFT JOIN sys_cell sc ON sd.id = sc.dish_id AND sc.del_flag = 0
        LEFT JOIN t_procedure_dish tpd ON sd.id = tpd.dish_id AND tpd.image_path = :imagePath
        LEFT JOIN t_embryo te ON sc.id = te.cell_id AND sc.del_flag = 0 AND tpd.procedure_id = te.procedure_id
        LEFT JOIN t_procedure tp ON tp.id = tpd.procedure_id
        LEFT JOIN t_patient p ON tp.patient_id = p.id
        LEFT JOIN sys_dict dict ON tp.insemi_type_id = dict.dict_key AND dict.dict_class = 'insemi_type'
        LEFT JOIN (
        SELECT t1.procedure_id, COUNT(DISTINCT t1.id) embryoSum
        FROM t_embryo t1
        LEFT JOIN sys_dish t3 ON t3.incubator_id = :incubatorId AND t3.del_flag = 0
        LEFT JOIN t_procedure_dish t2 ON t1.procedure_id = t2.procedure_id
        WHERE t2.dish_id = t3.id AND t2.image_path = :imagePath
        GROUP BY t1.procedure_id) a ON tpd.procedure_id = a.procedure_id
        WHERE sd.incubator_id = :incubatorId AND sd.del_flag = 0
        GROUP BY sc.dish_id""")
    print(sql)
    
    # 执行sql得出结果
    result = db.session.execute(sql,params)
    sql_result = result.fetchall()
    
    return sql_result

def findImagePathByProcedureId(procedureId):
    sql = text('''select tpd.image_path from t_procedure_dish tpd where tpd.procedure_id = :procedureId limit 0,1''')
    print(sql)
    
    params = {'procedureId':procedureId}
    # 执行sql得出结果
    result = db.session.execute(sql,params)
    data = result.fetchone()
    if data is None :
        imagePath = ''
    else :
        imagePath = data[0]
    return imagePath
 
def findLatestImagePath(incubatorId):
    sql = text('''SELECT tpd.image_path
        FROM sys_dish sd
        left join t_procedure_dish tpd on sd.id = tpd.dish_id
        WHERE sd.incubator_id = :incubatorId AND sd.del_flag = 0
        order BY tpd.image_path desc limit 0,1''')
    print(sql)
    
    params = {'incubatorId':incubatorId}
    # 执行sql得出结果
    result = db.session.execute(sql,params)
    data = result.fetchone()
    if data is None :
        imagePath = ''
    else :
        imagePath = data[0]
    return imagePath
