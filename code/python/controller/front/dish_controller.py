from flask import Blueprint, jsonify,render_template
import logUtils
from app import login_required 
from entity.Embryo import Embryo
from flask_restful import reqparse

''' 皿视图 '''
dish_controller = Blueprint('dish_controller', __name__)
url_prefix = '/front/dish'

@dish_controller.route('/', methods=['GET'])
@login_required
def dishView():
    logUtils.info('dish_controller.dishView-跳转到皿视图页面')
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('dishCode', type=str)

    agrs = parser.parse_args()
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    dishCode = agrs['dishCode']
    return render_template('front/dish/dish.html', procedure_id=procedureId, dish_id=dishId, dishCode=dishCode)

"""跳转到根据皿ID获取胚胎评分表"""
@dish_controller.route('/emGrade/<string:dishId>', methods=['GET'])
@login_required
def emGrade(dishId):
    logUtils.info('dish_controller.emGrade-跳转到胚胎评分表')
    return render_template('front/dish/emGrade.html', dishId=dishId)

"""跳转到根据皿ID获取胚胎总览表"""
@dish_controller.route('/emAll/<string:dishId>', methods=['GET'])
@login_required
def emAll(dishId):
    logUtils.info('dish_controller.emAll-跳转到胚胎总览表')
    return render_template('front/dish/emAll.html', dishId=dishId)