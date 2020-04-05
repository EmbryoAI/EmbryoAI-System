# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Incubator(db.Model, mixin):
    __tablename__ = "sys_incubator"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    incubatorCode = db.Column("incubator_code", db.String(12))
    incubatorDescription = db.Column("incubator_description", db.String(200))
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    incubatorBrand = db.Column("incubator_brand", db.String(100), default="ASTEC")
    incubatorType = db.Column("incubator_type", db.String(100), default="iBIS")
    delFlag = db.Column("del_flag", db.Integer, default=0)
