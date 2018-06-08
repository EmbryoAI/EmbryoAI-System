# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Patient(db.Model, mixin):
    __tablename__ = "t_patient"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    idcardNo = db.Column("idcard_no", db.String(20))
    idcardTypeId = db.Column("idcard_type_id", db.String(32))
    patientName = db.Column("patient_name", db.String(50))
    birthdate = db.Column("birthdate", db.DateTime)
    country = db.Column("country", db.String(50))
    locationId = db.Column("location_id", db.String(32))
    address = db.Column("address", db.String(500))
    email = db.Column("email", db.String(200))
    mobile = db.Column("mobile", db.String(30))
    createTime = db.Column("create_time", db.DateTime)
    updateTime = db.Column("update_time", db.DateTime)
    delFlag = db.Column("del_flag", db.Integer, default=0)

