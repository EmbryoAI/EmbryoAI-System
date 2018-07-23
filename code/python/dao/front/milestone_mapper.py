# -*- coding: utf8 -*-

from app import db
from entity.Milestone import Milestone
from entity.MilestoneData import MilestoneData
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc

def insertMilestone(milestone,milestoneData):
    try :
        db.session.add(milestone)
        db.session.add(milestoneData)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('设置里程碑时发生错误!', e.message, e)
    
def updateMilestone(milestone,milestoneData):
    try :
        sql = text("""
            UPDATE t_milestone 
            SET
            embryo_id =:embryoId, 
            milestone_id =:milestoneId, 
            milestone_time =:milestoneTime, 
            milestone_elapse =:milestoneElapse, 
            user_id =:userId, 
            milestone_type =:milestoneType, 
            milestone_path =:milestonePath
            WHERE id =:id
        """)
        
        sql2 = text("""
            UPDATE embryoai_system_db.t_milestone_data 
                SET
                milestone_stage =:milestoneStage , 
                pn_id =:pnId , 
                cell_count =:cellCount , 
                even_id =:evenId , 
                fragment_id =:fragmentId , 
                grade_id =:gradeId , 
                diameter =:diameter , 
                AREA =:area , 
                thickness =:thickness , 
                milestone_score =:milestoneScore , 
                user_id =:userId , 
                memo =:memo
                WHERE milestone_id =:milestoneId  
        """)
        
        db.session.execute(sql, milestone)
        db.session.execute(sql2, milestoneData)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print_exc()
        raise DatabaseError('设置里程碑时发生错误!', e.message, e)

#动态条件查询里程碑对象
def getMilestoneByEmbryoId(sqlCondition,filters):
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
    return reslt