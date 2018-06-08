# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Milestone(db.Model, mixin):
    __tablename__ = "t_milestone"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    embryoId = db.Column("embryo_id", db.String(32))
    milestoneId = db.Column("milestone_id", db.String(32))
    milestoneTime = db.Column("milestone_time", db.DateTime)
    milestoneElapse = db.Column("milestone_elapse", db.Integer)
    userId = db.Column("user_id", db.String(32))
    milestoneType = db.Column("milestone_type", db.Integer)
    milestonePath = db.Column("milestone_path", db.String(500))

