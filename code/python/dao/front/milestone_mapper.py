# -*- coding: utf8 -*-

from app import db
from entity.Milestone import Milestone
from entity.MilestoneData import MilestoneData
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
import dao.front.dict_dao as dict_dao
from pyknow import *
from functools import partial
import time
import datetime
import dao.front.rule_dao as rule_dao
import dao.front.embryo_mapper as embryo_mapper
import knowledge.embryo_score as embryo_score
from common import get_serie_time_hours

def insertMilestone(milestone,milestoneData,procedure,cap_start_time):
    try :
        countMilestoneScore(milestone,milestoneData,procedure,cap_start_time)#计算节点分数
        db.session.add(milestone)
        db.session.add(milestoneData)
        embryoScore = updateEmbryoScore(milestone.embryoId);#修改胚胎表总分
        db.session.commit()
        return milestoneData.milestoneScore,embryoScore
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('设置里程碑时发生错误!', e.message, e)
    finally:
        db.session.remove()
    
def updateMilestone(milestone,milestoneData,procedure,cap_start_time):
    try :
        countMilestoneScore(milestone,milestoneData,procedure,cap_start_time)#计算节点分数
        sql = text("""
            UPDATE t_milestone 
            SET
            embryo_id =:embryoId, 
            milestone_id =:milestoneId, 
            milestone_time =:milestoneTime, 
            milestone_elapse =:milestoneElapse, 
            user_id =:userId, 
            milestone_type =:milestoneType, 
            milestone_path =:milestonePath, 
            thumbnail_path =:thumbnailPath
            WHERE id =:id
        """)
        
        sql2 = text("""
            UPDATE t_milestone_data 
                SET
                milestone_stage =:milestoneStage , 
                pn_id =:pnId , 
                cell_count =:cellCount , 
                even_id =:evenId , 
                fragment_id =:fragmentId , 
                grade_id =:gradeId , 
                inner_diameter =:innerDiameter , 
                inner_area =:innerArea, 
                zona_thickness =:zonaThickness, 
                milestone_score =:milestoneScore , 
                user_id =:userId , 
                memo =:memo ,
                outer_area =:outerArea ,
                outer_diameter =:outerDiameter ,
                expansion_area =:expansionArea 
                WHERE milestone_id =:milestoneId  
        """)
        
        db.session.execute(sql, milestone.to_dict())
        db.session.execute(sql2, milestoneData.to_dict())
        embryoScore = updateEmbryoScore(milestone.embryoId);#修改胚胎表总分
        db.session.commit()
        return milestoneData.milestoneScore,embryoScore
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('设置里程碑时发生错误!', e.message, e)
    finally:
        db.session.remove()

#计算里程碑节点分
def countMilestoneScore(milestone,milestoneData,procedure,cap_start_time):
    #评分设置，首先查询出当前周期对应的评分规则
    rule = rule_dao.getRuleById(procedure.embryoScoreId,milestoneData.userId)
    print("procedure.embryoScoreId："+procedure.embryoScoreId)
    print("milestoneData.userId："+milestoneData.userId)
    print(rule.dataJson)
    engine = embryo_score.init_engine(rule.dataJson)
    #获取当前胚胎的的胚胎形态
    stageDict =  dict_dao.getDictByClassAndKey("milestone",milestone.milestoneId);
    pnIdDict =  dict_dao.getDictByClassAndKey("pn",milestoneData.pnId);
    cellDict =  dict_dao.getDictByClassAndKey("cell",milestoneData.cellCount);
    evenDict =  dict_dao.getDictByClassAndKey("even",milestoneData.evenId);
    fragmentDict =  dict_dao.getDictByClassAndKey("fragment",milestoneData.fragmentId);
    gradeDict =  dict_dao.getDictByClassAndKey("grade",milestoneData.gradeId);
 
    engine = embryo_score.init_engine(rule.dataJson)
    
    cap_start_time = datetime.datetime.strptime(cap_start_time, "%Y%m%d%H%M%S")
    cap_start_time = cap_start_time.strftime("%Y-%m-%d %H:%M")
    insemiTime = procedure.insemiTime.strftime("%Y-%m-%d %H:%M")
    timeValue = get_serie_time_hours(insemiTime,cap_start_time,milestone.milestoneTime)
    #计算时间
    engine.declare(Fact(stage=stageDict.dictValue,condition="time", value=str(timeValue)))
    #计算节点
    if stageDict.dictValue == 'PN':
        engine.declare(Fact(stage=stageDict.dictValue,condition=pnIdDict.dictClass, value=pnIdDict.dictValue))
    elif stageDict.dictValue=="2C" or stageDict.dictValue=="3C" or stageDict.dictValue=="4C" or stageDict.dictValue=="5C" or stageDict.dictValue=="8C":    
         engine.declare(Fact(stage=stageDict.dictValue,condition=cellDict.dictClass, value=cellDict.dictValue))
         engine.declare(Fact(stage=stageDict.dictValue,condition=evenDict.dictClass, value=evenDict.dictValue))
         if stageDict.dictValue=="3C" or stageDict.dictValue=="4C" or stageDict.dictValue=="5C" or stageDict.dictValue=="8C":
            engine.declare(Fact(stage=stageDict.dictValue,condition=fragmentDict.dictClass, value=fragmentDict.dictValue))
         if stageDict.dictValue=="8C":
            engine.declare(Fact(stage=stageDict.dictValue,condition=gradeDict.dictClass, value=gradeDict.dictValue))
    engine.run()
    print(engine.score)
    milestoneData.milestoneScore=engine.score
#     embryo_mapper.updateEmbryoScore(embryoId,sumScore)

#保存胚胎总分
def updateEmbryoScore(embryoId):
    count_sql = text("""
            SELECT SUM(b.milestone_score)
                        FROM t_milestone a
                        LEFT JOIN t_milestone_data b
                        ON a.id = b.milestone_id
                        WHERE  a.embryo_id=:embryoId
    """)
    print(count_sql)
    # 计算总条数
    count_result = db.session.execute(count_sql,{"embryoId":embryoId})
    totalSize = count_result.fetchone()[0]
    
    sql = text("""
            UPDATE t_embryo SET embryo_score =:totalSize
            WHERE id=:embryoId
    """)
    db.session.execute(sql, {"totalSize":totalSize,"embryoId":embryoId})
    return totalSize
        
#动态条件查询里程碑对象
def getMilestoneByEmbryoId(sqlCondition,filters):
    reslt = None
    try :
        sql = text("""
                SELECT
                  a.id               AS id,
                  a.embryo_id        AS embryoId,
                  a.milestone_id     AS milestoneId,
                  b.dict_value       AS milestoneName,
                  a.milestone_time   AS milestoneTime,
                  a.milestone_elapse AS milestoneElapse,
                  user_id            AS userId,
                  a.milestone_type   AS milestoneType,
                  a.milestone_path   AS milestonePath
                FROM t_milestone a,
                  sys_dict b
                WHERE a.milestone_id = b.dict_key
                    AND b.dict_class = 'milestone'
                     """+sqlCondition+"""
            """)
        print(sql)
        # 计算总条数
        count_result = db.session.execute(sql,filters)
        reslt = count_result.fetchone()
    except Exception as e:
        return reslt
    finally:
        db.session.remove()
    return reslt

#根据胚胎ID获取它的所有里程碑节点
def queryMilestoneList(embryoId):
    milestoneList = None
    try:
         milestoneList = db.session.query(Milestone).filter(Milestone.embryoId == embryoId).order_by('milestone_time').all()
    except Exception as e:
        return milestoneList
    finally:
         db.session.remove()
    return milestoneList

#根据胚胎ID获取里程碑节点
def getMilestone(embryoId):
    try:
        sql = text("""
                SELECT sd.`dict_value` AS milestone_type, tm.`embryo_id` AS embryo_id, tm.`milestone_time` AS seris  
                FROM `t_milestone` tm 
                LEFT JOIN `sys_dict` sd 
                ON tm.`milestone_id` = sd.`dict_key` 
                WHERE sd.`dict_class` = 'milestone'  
                AND tm.`embryo_id` = '""" + embryoId + """' 
            """)
        print(sql)
        return db.session.execute(sql).fetchall()
    except Exception as e:
        raise DatabaseError("根据胚胎ID查询里程碑信息异常",e.message,e)
        return None
    finally:
         db.session.remove()

#根据胚胎ID获取所有里程碑节点的胚胎形态
def queryEmbryoForm(embryoId):
    try:
        sql = text("""
            SELECT c.dict_value AS 'stage',a.milestone_time AS milestoneTime,d.dict_class AS 'condition',d.dict_value AS 'value'
            ,d1.dict_class AS 'condition1',d1.dict_value AS 'value1'
            ,d2.dict_class AS 'condition2',d2.dict_value AS 'value2'
            ,d3.dict_class AS 'condition3',d3.dict_value AS 'value3'
            ,d4.dict_class AS 'condition4',d4.dict_value AS 'value4'
            FROM t_milestone a
            LEFT JOIN t_milestone_data b
            ON a.id = b.milestone_id
            LEFT JOIN sys_dict c
            ON a.milestone_id=c.dict_key AND c.dict_class='milestone'
            LEFT JOIN sys_dict d
            ON b.pn_id=d.dict_key AND d.dict_class='pn'
            LEFT JOIN sys_dict d1
            ON b.cell_count=d1.dict_key AND d1.dict_class='cell'
            LEFT JOIN sys_dict d2
            ON b.even_id=d2.dict_key AND d2.dict_class='even'
            LEFT JOIN sys_dict d3
            ON b.fragment_id=d3.dict_key AND d3.dict_class='fragment'
            LEFT JOIN sys_dict d4
            ON b.grade_id=d4.dict_key AND d4.dict_class='grade'
            WHERE  a.embryo_id  = :embryoId
            """)
        print(sql)
        return db.session.execute(sql, {'embryoId':embryoId}).fetchall()
    except Exception as e:
        raise DatabaseError("根据胚胎ID获取所有里程碑节点的胚胎形态异常",e.message,e)
        return None
    finally:
         db.session.remove()