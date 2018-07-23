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
    
def getMilestoneByEmbryoId(embryoId):
    return db.session.query(Milestone).filter(Milestone.embryoId == embryoId).one_or_none()