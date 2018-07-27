# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Dict(db.Model, mixin):
    __tablename__ = "sys_dict"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    dictClass = db.Column("dict_class", db.String(50))
    dictKey = db.Column("dict_key", db.String(100))
    dictValue = db.Column("dict_value", db.String(200))
    dictSpare = db.Column("dict_spare", db.String(50))

