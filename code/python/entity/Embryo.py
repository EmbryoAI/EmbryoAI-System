# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class Embryo(db.Model, mixin):
    __tablename__ = "t_embryo"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    embryoIndex = db.Column("embryo_index", db.Integer)
    procedureId = db.Column("procedure_id", db.String(32))
    cellId = db.Column("cell_id", db.String(32))
    embryoScore = db.Column("embryo_score", db.Float)
    embryoFateId = db.Column("embryo_fate_id", db.String(32))
