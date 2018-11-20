#!/usr/bin/env python
#coding:utf8


class WellResult():

     def __init__(self, code, msg, well_list, milestone_list, last_seris):
        self.code = code
        self.msg = msg
        self.well_list = well_list
        self.milestone_list = milestone_list
        self.last_seris = last_seris