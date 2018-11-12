#!/bin/env python
# -*- coding: utf8 -*-

from pyknow import *
from functools import partial
# from app import logger

rule_json = '''{
	"PN": [{
		"index": "675d9ba0df1211e8b8950242ac120002",
		"condition": "pn",
		"symbol": "=",
		"valueKey": "2",
		"value": "2PN",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "729f0c6adf1211e883ff0242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "12",
		"value": "12",
		"score": "20",
		"weight": "1.0"
	}],
	"2C": [{
		"index": "801c79a4df1211e890220242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "2",
		"value": "2C",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "95a1b334df1211e883d70242ac120002",
		"condition": "even",
		"symbol": "=",
		"valueKey": "0",
		"value": "均匀",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "a254163adf1211e8a4730242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "18",
		"value": "18",
		"score": "20",
		"weight": "1.0"
	}],
	"3C": [{
		"index": "ac684222df1211e88f4e0242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "3",
		"value": "3C",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "b6799888df1211e8ba3a0242ac120002",
		"condition": "even",
		"symbol": "=",
		"valueKey": "0",
		"value": "均匀",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "c3f17968df1211e890390242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "1",
		"value": "<5%",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "cee46772df1211e8af800242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "2",
		"value": "5%-10%",
		"score": "15",
		"weight": "1.0"
	}, {
		"index": "db20b19edf1211e88ec40242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "3",
		"value": "10%-20%",
		"score": "10",
		"weight": "1.0"
	}, {
		"index": "ea214d66df1211e89c0c0242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "24",
		"value": "24",
		"score": "20",
		"weight": "1.0"
	}],
	"4C": [{
		"index": "f58ca4fcdf1211e89fb30242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "4",
		"value": "4C",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "02c18b7edf1311e8b4b40242ac120002",
		"condition": "even",
		"symbol": "=",
		"valueKey": "0",
		"value": "均匀",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "0c90e910df1311e893f10242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "1",
		"value": "<5%",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "195e8206df1311e8856d0242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "3",
		"value": "5%-10%",
		"score": "15",
		"weight": "1.0"
	}, {
		"index": "25dd981edf1311e8805a0242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "3",
		"value": "10%-20%",
		"score": "10",
		"weight": "1.0"
	}, {
		"index": "3dd849d2df1311e884c90242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "36",
		"value": "36",
		"score": "20",
		"weight": "1.0"
	}],
	"5C": [{
		"index": "4bd1b636df1311e8a95b0242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "5",
		"value": "5C",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "5916b148df1311e88b850242ac120002",
		"condition": "even",
		"symbol": "=",
		"valueKey": "0",
		"value": "均匀",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "6332bcd0df1311e898de0242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "1",
		"value": "<5%",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "7002d904df1311e889a10242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "2",
		"value": "5%-10%",
		"score": "15",
		"weight": "1.0"
	}, {
		"index": "7a58c3a0df1311e890260242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "3",
		"value": "10%-20%",
		"score": "10",
		"weight": "1.0"
	}, {
		"index": "a9d5194edf1311e8ba400242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "48",
		"value": "48",
		"score": "20",
		"weight": "1.0"
	}],
	"8C": [{
		"index": "b5beaaaedf1311e8a8550242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "8",
		"value": "8C",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "c9aceaf8df1311e8b40d0242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "7",
		"value": "7C",
		"score": "15",
		"weight": "1.0"
	}, {
		"index": "d5dbe3cedf1311e8a9020242ac120002",
		"condition": "cell",
		"symbol": "=",
		"valueKey": "6",
		"value": "6C",
		"score": "10",
		"weight": "1.0"
	}, {
		"index": "beb93d3edf1511e89e410242ac120002",
		"condition": "even",
		"symbol": "=",
		"valueKey": "0",
		"value": "均匀",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "c94726b2df1511e8a2ba0242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "1",
		"value": "<5%",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "db75be16df1511e8b44b0242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "2",
		"value": "5%-10%",
		"score": "15",
		"weight": "1.0"
	}, {
		"index": "e7aac172df1511e8b89b0242ac120002",
		"condition": "fragment",
		"symbol": "=",
		"valueKey": "3",
		"value": "10%-20%",
		"score": "10",
		"weight": "1.0"
	}, {
		"index": "f5357e7cdf1511e880b70242ac120002",
		"condition": "grade",
		"symbol": "=",
		"valueKey": "1",
		"value": "I",
		"score": "50",
		"weight": "1.0"
	}, {
		"index": "ff96b96cdf1511e887ce0242ac120002",
		"condition": "grade",
		"symbol": "=",
		"valueKey": "2",
		"value": "II",
		"score": "20",
		"weight": "1.0"
	}, {
		"index": "158c9836df1611e89cbe0242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "60",
		"value": "60",
		"score": "20",
		"weight": "1.0"
	}],
	"囊胚": [{
		"index": "2400bf1edf1611e88ad00242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "85",
		"value": "85",
		"score": "20",
		"weight": "1.0"
	}],
	"扩张囊胚": [{
		"index": "35a141c6df1611e882450242ac120002",
		"condition": "time",
		"symbol": "<=",
		"valueKey": "96",
		"value": "96",
		"score": "20",
		"weight": "1.0"
	}]
}'''

class EmbryoScore(KnowledgeEngine):
	''' 胚胎自动评分知识引擎类 '''
	score = 0
	@classmethod
	def removeAllRules(cls):
		''' 移除类中所有的规则，规则方法以rule开头 '''
		for m in [attr for attr in cls.__dict__ if attr.startswith('rule')]:
			delattr(cls, m)

def parse_json_rules(rule_json):
	''' 将json字符串内容加载到知识引擎中 
		@param rule_json: 从数据库中读取到的评分规则json字符串
	'''
	import json
	rules = json.loads(rule_json)
	sal = 100 # 规则优先级
	index = 0	# 规则属性序号
	for stage in rules: # 循环读取胚胎阶段
		for rule_item in rules[stage]: # 循环读取每个阶段中的每个规则
			# 需要进行判断的条件包括：胚胎阶段 stage，判断内容 condition，真实的值 value
			rule = {'condition': rule_item['condition']}
			rule['stage'] = stage
			# 目前支持的条件判断符号
			if rule_item['symbol'] not in ('=', '<', '<=', '>', '>='):
				continue
			# 5种不同的判断
			def _cond(value, symbol):
				if symbol == '=': return EQ(value)
				if symbol == '<': return LT(value)
				if symbol == '<=': return LE(value)
				if symbol == '>': return GT(value)
				if symbol == '>=': return GE(value)

			# 计算分值的闭包方法
			def _add_partial(score, weight):
				def _add(self, **kwargs):
					s, w = int(score), float(weight)
					self.score += s * w
				return _add
			# 构建Rule处理方法，并将其添加到EmbryoScore类中
			R = Rule(AND(Fact(**rule, value=MATCH.value & 
					_cond(rule_item['value'], rule_item['symbol']))),
					salience=sal)(_add_partial(score=rule_item['score'], 
					weight=rule_item['weight']))
			setattr(EmbryoScore, f'rule{index}', R)

			index += 1	# Rule序号递增
			sal -= 1 # 优先级递减

def init_engine(rule_json):
	''' 初始化规则引擎
		@param rule_json: 从数据库读取出来的规则json字符串
	'''
	EmbryoScore.removeAllRules()
	parse_json_rules(rule_json)
	engine = EmbryoScore()
	engine.reset()
	return engine

import unittest

class ScoreTest(unittest.TestCase):
	def test(self):
		engine = init_engine(rule_json)
		engine.declare(Fact(condition='pn', stage='PN', value='2PN'))
		engine.declare(Fact(stage='4C', condition='cell', value='4C'))
		engine.declare(Fact(stage='4C', condition='fragment', value='10%-20%'))
		engine.declare(Fact(stage='8C', condition='time', value='32'))
		engine.declare(Fact(stage='8C', condition='grade', value='III'))
		engine.run()
		print(engine.score)
		self.assertEqual(engine.score, 70)


if __name__ == '__main__':
    unittest.main()