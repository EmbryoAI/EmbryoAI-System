#!/usr/bin/env python
# coding:utf8


class RestResult:
    def __init__(self, code, msg, count, data):
        self.code = code
        self.msg = msg
        self.count = count
        self.data = data
