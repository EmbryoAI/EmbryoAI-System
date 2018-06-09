# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class MilestoneData(db.Model, mixin):
    __tablename__ = "t_milestone_data"

    milestoneId = db.Column("milestone_id", db.String(32), primary_key=True, nullable=False)
    milestoneStage = db.Column("milestone_stage", db.Integer)
    pnId = db.Column("pn_id", db.String(32))
    cellCount = db.Column("cell_count", db.Integer)
    evenId = db.Column("even_id", db.String(32))
    fragmentId = db.Column("fragment_id", db.String(255))
    gradeId = db.Column("grade_id", db.String(255))
    diameter = db.Column("diameter", db.Integer)
    area = db.Column("area", db.Integer)
    thickness = db.Column("thickness", db.Integer)
    milestoneScore = db.Column("milestone_score", db.Float)
    userId = db.Column("user_id", db.String(32))
    memo = db.Column("memo", db.String(500))

