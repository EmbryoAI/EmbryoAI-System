# -*- coding: utf8 -*-

from sqlalchemy_serializer import SerializerMixin as mixin
from app import db


class RuleCriteria(db.Model, mixin):
    __tablename__ = "t_rule_criteria"

    id = db.Column("id", db.String(32), primary_key=True, nullable=False)
    ruleId = db.Column("rule_id", db.String(32))
    milestoneId = db.Column("milestone_id", db.String(32))
    criteriaTypeId = db.Column("criteria_type_id", db.String(32))
    criteriaFieldId = db.Column("criteria_field_id", db.String(32))
    criteriaOpId = db.Column("criteria_op_id", db.String(32))
    criteriaValue = db.Column("criteria_value", db.String(32))
    criteriaOrder = db.Column("criteria_order", db.Integer)
    criteriaScore = db.Column("criteria_score", db.Integer)
    criteriaWeight = db.Column("criteria_weight", db.Float, default=1)
