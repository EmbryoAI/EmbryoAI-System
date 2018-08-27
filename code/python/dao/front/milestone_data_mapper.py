# -*- coding: utf8 -*-

from app import db
from entity.MilestoneData import MilestoneData
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
    
def getMilestoneData(milestoneId):
    try:
        return db.session.query(MilestoneData).filter(MilestoneData.milestoneId == milestoneId).one_or_none()
    except Exception as e:
        raise DatabaseError('根据主键ID查询病历时异常', e.message, e)
        return None
    finally:
        db.session.remove()