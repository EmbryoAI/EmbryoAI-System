#!/usr/bin/env python
#coding:utf8


class SeriesResult():

     def __init__(self, code, msg, series, current_series, last_series, milestone_list):
        self.code = code
        self.msg = msg
        self.series = series
        self.current_series = current_series
        self.last_series = last_series
        self.milestone_list = milestone_list