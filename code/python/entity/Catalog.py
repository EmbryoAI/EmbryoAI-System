#!/usr/bin/env python
# coding:utf8


class Catalog:
    def __init__(
        self,
        incubator,
        dish_list,
        patient_name,
        collection_date,
        embryo_number,
        procedure_number,
        memo,
    ):
        self.incubator = incubator
        self.dish_list = dish_list
        self.patient_name = patient_name
        self.collectionDate = collection_date
        self.embryo_number = embryo_number
        self.procedure_number = procedure_number
        self.memo = memo
