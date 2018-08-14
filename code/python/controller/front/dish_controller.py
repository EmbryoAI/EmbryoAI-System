from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 
from entity.Embryo import Embryo
from flask_restful import reqparse

''' 皿视图 '''
dish_controller = Blueprint('dish_controller', __name__)
url_prefix = '/front/dish'

@dish_controller.route('/', methods=['GET'])
@login_required
def dishView():
    logger().info('dish_controller.皿视图页面')

    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('embryoId', type=str)

    agrs = parser.parse_args()
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    embryoId = agrs['embryoId']
    return render_template('front/dish/dish.html', procedure_id=procedureId, dish_id=dishId, embryo_id=embryoId)