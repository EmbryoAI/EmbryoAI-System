from app import db
from entity.Dish import Dish
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
import logUtils


def queryById(dishId):
    try:
        dish = (
            db.session.query(Dish)
            .filter(Dish.id == dishId, Dish.delFlag == 0)
            .one_or_none()
        )
    except Exception as e:
        logUtils.error(f"使用皿ID查询皿信息时发生错误: {e}")
        return None
    finally:
        db.session.remove()
    return dish


def findDishByIncubatorId(params):
    try:
        sql = text(
            """
            SELECT sd.id AS dishId,sd.dish_code AS dishCode, COUNT(DISTINCT te.cell_id) AS embryoCount,tp.id procedureId,
            p.patient_name name,tp.patient_age age, CONCAT(tp.insemi_time) insemiTime,tpd.image_path imagePath,dict.dict_value insemiType, 
            CONCAT('D', DATEDIFF(IF(tp.cap_end_time,tp.cap_end_time, NOW()),tp.insemi_time)) AS stage, IFNULL(a.embryoSum,0) embryoSum
            FROM sys_dish sd
            LEFT JOIN sys_cell sc ON sd.id = sc.dish_id AND sc.del_flag = 0
            LEFT JOIN t_procedure_dish tpd ON sd.id = tpd.dish_id AND tpd.image_path = :imagePath
            LEFT JOIN t_embryo te ON sc.id = te.cell_id AND sc.del_flag = 0 AND tpd.procedure_id = te.procedure_id
            LEFT JOIN t_procedure tp ON tp.id = tpd.procedure_id and tp.del_flag = 0
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
            GROUP BY sc.dish_id"""
        )
        logUtils.info(sql)
        # 执行sql得出结果
        result = db.session.execute(sql, params)
        sql_result = result.fetchall()

        return sql_result
    except Exception as e:
        raise DatabaseError("根据培养箱id查询该培养箱下的培养皿信息发送错误", e.message, e)
        return None
    finally:
        db.session.remove()


def findImagePathByProcedureId(procedureId):
    try:
        sql = text(
            """
            select tpd.image_path from t_procedure_dish tpd 
            LEFT JOIN t_procedure tp ON tpd.procedure_id = tp.id 
            where tpd.procedure_id = :procedureId 
            AND tp.del_flag = 0 
            limit 0,1
        """
        )
        logUtils.info(sql)
        params = {"procedureId": procedureId}
        # 执行sql得出结果
        result = db.session.execute(sql, params)
        data = result.fetchone()
        if data is None:
            imagePath = ""
        else:
            imagePath = data[0]
        return imagePath
    except Exception as e:
        raise DatabaseError("查询某个周期的最新采集目录时发生错误", e.message, e)
        return None
    finally:
        db.session.remove()


def findLatestImagePath(incubatorId):
    try:
        sql = text(
            """SELECT tpd.image_path
            FROM sys_dish sd
            left join t_procedure_dish tpd on sd.id = tpd.dish_id
            LEFT JOIN t_procedure tp ON tpd.procedure_id = tp.id
            WHERE sd.incubator_id = :incubatorId 
            AND sd.del_flag = 0 
            AND tp.del_flag = 0
            order BY tpd.image_path desc limit 0,1"""
        )
        logUtils.info(sql)
        params = {"incubatorId": incubatorId}
        # 执行sql得出结果
        result = db.session.execute(sql, params)
        data = result.fetchone()
        if data is None:
            imagePath = ""
        else:
            imagePath = data[0]
        return imagePath
    except Exception as e:
        raise DatabaseError("查询培养箱下的最新采集目录时发生错误", e.message, e)
        return None
    finally:
        db.session.remove()


def queryWellIdAndImagePath(procedureId, dishCode):
    try:
        sql = text(
            """select sc.cell_code wellCode,tps.image_path imagePath from t_procedure_dish tps 
        left join sys_dish sd on tps.dish_id = sd.id 
        left join sys_cell sc on tps.dish_id = sc.dish_id 
        left join t_procedure tp on tps.procedure_id = tp.id 
        left join t_embryo te on te.procedure_id = tps.procedure_id and te.cell_id = sc.id 
        where tps.procedure_id = :procedureId
        and sd.dish_code = :dishCode
        and sd.del_flag = 0  
        and sc.del_flag = 0 
        and tp.del_flag = 0
        limit 0,1"""
        )
        logUtils.info(sql)
        params = {"dishCode": dishCode, "procedureId": procedureId}
        result = db.session.execute(sql, params)
        data = result.fetchone()
        if data is not None:
            wellCode = data[0]
            imagePath = data[1]
        return wellCode, imagePath
    except Exception as e:
        raise DatabaseError("查询培养箱下的最新采集目录时发生错误", e.message, e)
        return None, None
    finally:
        db.session.remove()


def getByDishCode(dishCode):
    try:
        return db.session.query(Dish).filter(Dish.dishCode == dishCode).one_or_none()
    except Exception as e:
        raise DatabaseError("getByDishCode失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def save(dish):
    try:
        db.session.merge(dish)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError("新增培养皿数据时发生错误", e.message, e)
    finally:
        db.session.remove()


def queryDishByImagePath(imagePath):
    try:
        sql = text(
            """
            SELECT si.id incubatorId,si.incubator_code incubatorCode, sd.id dishId,sd.dish_code dishCode
            FROM sys_dish sd
            LEFT JOIN t_procedure_dish tpd ON sd.id = tpd.dish_id
            LEFT JOIN sys_incubator si ON sd.incubator_id = si.id
            WHERE tpd.image_path = :imagePath  and  sd.del_flag = 0 
            limit 0,3
        """
        )
        logUtils.info(sql)
        params = {"imagePath": imagePath}
        print(params)
        result = db.session.execute(sql, params)
        data = result.fetchall()
        return data
    except Exception as e:
        raise DatabaseError("查询培养箱下的最新采集目录时发生错误", e.message, e)
        return None
    finally:
        db.session.remove()


"""根据皿ID获取胚胎评分表"""


def emGrade(dishId):
    try:
        sql = text(
            """
          SELECT
              c.cell_code    AS   cellCode,
              e.embryo_score AS embryoScore
            FROM t_embryo e
              LEFT JOIN sys_cell c
                ON e.cell_id = c.id
            WHERE c.dish_id =:dishId
        """
        )
        logUtils.info(sql)
        params = {"dishId": dishId}
        result = db.session.execute(sql, params)
        data = result.fetchall()
        return data
    except Exception as e:
        raise DatabaseError("根据皿ID获取胚胎评分表时发生错误", e.message, e)
        return None
    finally:
        db.session.remove()


"""根据皿ID获取胚胎总览表"""


def emAll(dishId):
    try:
        sql = text(
            """
            SELECT e.embryo_index AS codeIndex, 
            SUM(da.pn_id) AS pnId,
                GROUP_CONCAT(dict1.dict_value,"#",m.thumbnail_path,"#",m.milestone_time ORDER BY m.milestone_time) lcb,
                e.embryo_score AS score ,dict2.dict_value AS embryoFate
                FROM t_embryo e
                LEFT JOIN t_procedure t
                ON e.procedure_id = t.id
                LEFT JOIN t_milestone m
                ON m.embryo_id = e.id
                LEFT JOIN t_milestone_data da
                ON m.id = da.milestone_id AND da.pn_id IS NOT NULL
                LEFT JOIN t_procedure_dish td
                ON t.id=td.procedure_id
            LEFT JOIN sys_dict dict1
            ON m.milestone_id = dict1.dict_key AND dict1.dict_class='milestone' 
            LEFT JOIN sys_dict dict2
            ON e.embryo_fate_id = dict2.dict_key AND dict2.dict_class='embryo_fate_type' 
                WHERE td.dish_id =:dishId
                GROUP BY e.id
        """
        )
        logUtils.info(sql)
        params = {"dishId": dishId}
        result = db.session.execute(sql, params)
        data = result.fetchall()
        return data
    except Exception as e:
        raise DatabaseError("根据皿ID获取胚胎评分表时发生错误", e.message, e)
        return None
    finally:
        db.session.remove()


def getByIncubatorIdDishCode(incubatorId, dishCode):
    try:
        return (
            db.session.query(Dish)
            .filter(Dish.incubatorId == incubatorId, Dish.dishCode == dishCode)
            .one_or_none()
        )
    except Exception as e:
        raise DatabaseError("getByIncubatorIdDishCode失败！", e.message, e)
        return None
    finally:
        db.session.remove()


def queryTop3Dish():
    try:
        sql = text(
            """
            SELECT si.id incubatorId,si.incubator_code incubatorCode, sd.id dishId,sd.dish_code dishCode,tpd.image_path imagePath
            FROM sys_dish sd
            LEFT JOIN t_procedure_dish tpd ON sd.id = tpd.dish_id
            left join t_procedure tp on tpd.procedure_id = tp.id
            LEFT JOIN sys_incubator si ON sd.incubator_id = si.id
            WHERE sd.del_flag = 0 and tp.del_flag = 0
            ORDER BY tpd.image_path DESC
            LIMIT 0,3
        """
        )
        logUtils.info(sql)
        result = db.session.execute(sql)
        data = result.fetchall()
        return data
    except Exception as e:
        raise DatabaseError("查询培养箱下的最新采集目录时发生错误", e.message, e)
        return None
    finally:
        db.session.remove()
