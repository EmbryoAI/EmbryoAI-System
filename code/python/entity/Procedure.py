# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Procedure(db.Model, mixin):
    __tablename__ = "t_procedure"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    patientId = db.Column("patient_id", db.String(32))
    userId = db.Column("user_id", db.String(32))
    patientAge = db.Column("patient_age", db.Integer)
    patientHeight = db.Column("patient_height", db.Float)
    patientWeight = db.Column("patient_weight", db.Float)
    patientHeightUnit = db.Column("patient_height_unit", db.String(10), default='cm')
    patientWeightUnit = db.Column("patient_weight_unit", db.String(10), default='kg')
    cycleTypeId = db.Column("cycle_type_id", db.String(32), default='f37b4a8a6bed11e8b4910242ac110002')
    freshCycleCount = db.Column("fresh_cycle_count", db.Integer, default=1)
    ecTime = db.Column("ec_time", db.DateTime)
    ecCount = db.Column("ec_count", db.String(255))
    insemiTime = db.Column("insemi_time", db.DateTime)
    insemiTypeId = db.Column("insemi_type_id", db.String(32), default='f37b46026bed11e8b4910242ac110002')
    capStartTime = db.Column("cap_start_time", db.DateTime)
    capEndTime = db.Column("cap_end_time", db.DateTime)
    zCount = db.Column("z_count", db.Integer)
    zSlice = db.Column("z_slice", db.Integer)
    state = db.Column("state", db.String(255))
    memo = db.Column("memo", db.String(500))
    delFlag = db.Column("del_flag", db.Integer, default=0)
    medicalRecordNo = db.Column("medical_record_no", db.String(255))
    embryoScoreId = db.Column("embryo_score_id", db.String(32))
