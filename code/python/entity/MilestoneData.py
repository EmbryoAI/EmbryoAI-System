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
    innerDiameter = db.Column("inner_diameter", db.Integer)
    innerArea = db.Column("inner_area", db.Integer)
    outerDiameter = db.Column("outer_diameter", db.Integer)
    outerArea = db.Column("outer_area", db.Integer)
    expansionArea = db.Column("expansion_area", db.Integer)
    zonaThickness = db.Column("zona_thickness", db.Integer)
    milestoneScore = db.Column("milestone_score", db.Float)
    userId = db.Column("user_id", db.String(32))
    memo = db.Column("memo", db.String(500))

