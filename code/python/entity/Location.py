# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Location(db.Model, mixin):
    __tablename__ = "sys_location"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    locationName = db.Column("location_name", db.String(50))
    soleName = db.Column("sole_name", db.String(255))
    parentId = db.Column("parent_id", db.String(6))
    locationLevel = db.Column("location_level", db.Integer)
