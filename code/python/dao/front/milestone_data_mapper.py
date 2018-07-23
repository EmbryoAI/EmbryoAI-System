# -*- coding: utf8 -*-

from app import db
from entity.MilestoneData import MilestoneData
from sqlalchemy.exc import DatabaseError
from sqlalchemy import text
from traceback import print_exc
    
def getMilestoneData(milestoneId):
    return db.session.query(MilestoneData).filter(MilestoneData.milestoneId == milestoneId).one_or_none()