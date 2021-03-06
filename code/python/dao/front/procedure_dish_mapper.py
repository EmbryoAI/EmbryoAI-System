from sqlalchemy import text
from app import db
from entity.ProcedureDish import ProcedureDish
import logUtils


def queryByProcedureIdAndDishId(procedureId, dishId):
    try:
        procedureDish = (
            db.session.query(ProcedureDish)
            .filter(
                ProcedureDish.procedureId == procedureId, ProcedureDish.dishId == dishId
            )
            .one_or_none()
        )
        return procedureDish
    except Exception as e:
        logUtils.error(f"找不到对应周期和皿的数据：{e}")
        return None
    finally:
        db.session.remove()


def save(procedureDish):
    try:
        db.session.merge(procedureDish)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logUtils.error(f"新增周期与培养皿关联数据时发生错误: {e}")
    finally:
        db.session.remove()


def queryNewestImagesInfo():
    try:
        count_sql = text(
            """
            SELECT tpd.image_path imagePath
            FROM t_procedure_dish tpd
            LEFT JOIN t_procedure tp ON tpd.procedure_id = tp.id
            WHERE tp.del_flag = 0
            ORDER BY tpd.image_path DESC
            LIMIT 0,1
        """
        )
        logUtils.debug(count_sql)
        # 计算总条数
        count_result = db.session.execute(count_sql)
        data = count_result.fetchone()
        logUtils.debug(f"查询最新采集采集目录路径: {data}")
        # if data is not None:
        #     imagePath = data[0]
        # return imagePath
        return data[0] if data else None
    except Exception as e:
        logUtils.error(f"查询最新采集时间及培养箱信息: {e}")
        return None
    finally:
        db.session.remove()


def queryByImagePathAndDishId(imagePath, dishId):
    try:
        sql = text(
            """
            SELECT 
                tpd.dish_id AS dishId,
                tpd.id AS id,
                tpd.image_path AS imagePath,
                tpd.procedure_id AS procedureId
            FROM t_procedure_dish tpd 
            LEFT JOIN t_procedure tp 
            ON tpd.procedure_id = tp.id
            WHERE tpd.dish_id = :dishId 
            AND tpd.image_path = :imagePath 
            AND tp.del_flag = 0
        """
        )
        procedureDish = db.session.execute(
            sql, {"imagePath": imagePath, "dishId": dishId}
        ).one_or_none()
        return procedureDish
        # procedureDish =  db.session.query(ProcedureDish).filter(ProcedureDish.imagePath == imagePath,ProcedureDish.dishId == dishId).one_or_none()
    except Exception as e:
        logUtils.error(f"使用图像路径 {imagePath} 和皿ID {dishId} 查询周期皿信息错误: {e}")
        return None
    finally:
        db.session.remove()


def queryEmbryoId(imagePath, dishId, cellCode):
    try:
        sql = text(
            """
            SELECT tpd.procedure_id procedureId,te.id embryoId
            FROM t_procedure_dish tpd
            LEFT JOIN t_embryo te ON tpd.procedure_id = te.procedure_id
            LEFT JOIN sys_cell sc ON te.cell_id = sc.id AND tpd.dish_id = sc.dish_id 
            LEFT JOIN t_procedure tp ON tpd.procedure_id = tp.id 
            WHERE tpd.image_path = :imagePath AND sc.dish_id = :dishId 
            AND sc.cell_code = :cellCode AND tp.del_flag = 0
        """
        )
        logUtils.debug(sql)
        data = db.session.execute(
            sql, {"imagePath": imagePath, "dishId": dishId, "cellCode": cellCode}
        ).fetchone()
        logUtils.debug(f"查询结果：{data}")
        # if data is not None:
        #     procedureId = data[0]
        #     embryoId = data[1]
        return (data[0], data[1]) if data else (None, None)
    except Exception as e:
        logUtils.error(f"查询胚胎ID及病历发生异常: {e}")
        return None, None
    finally:
        db.session.remove()


def queryAllCatalog():
    try:
        sql = text(
            """
            SELECT tpd.image_path AS relation_catalog 
            FROM t_procedure_dish tpd 
            JOIN t_procedure tp 
            ON tpd.procedure_id = tp.id
            WHERE tp.`del_flag` = 0 
        """
        )
        logUtils.debug(sql)
        data = db.session.execute(sql).fetchall()
        return data
    except Exception as e:
        logUtils.error(f"查询所以关联病例采集目录信息错误: {e}")
        return None
    finally:
        db.session.remove()
