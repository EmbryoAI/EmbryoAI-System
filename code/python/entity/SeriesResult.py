#!/usr/bin/env python
#coding:utf8


class SeriesResult():

     def __init__(self, code, msg, series, last_series, embryo_id):
        self.code = code
        self.msg = msg
        self.series = series
        self.last_series = last_series
        self.embryo_id = embryo_id