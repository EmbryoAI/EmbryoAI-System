# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Feedback(db.Model, mixin):
    __tablename__ = "t_feedback"

    procedureId = db.Column("procedure_id", db.String(32), primary_key=True, nullable=False)
    biochemPregnancy = db.Column("biochem_pregnancy", db.Integer)
    clinicalPregnancy = db.Column("clinical_pregnancy", db.Integer)
    fetusCount = db.Column("fetus_count", db.Integer)
    userId = db.Column("user_id", db.String(32))
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    delFlag = db.Column("del_flag", db.Integer)

