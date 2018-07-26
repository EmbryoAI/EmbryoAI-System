from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 
from entity.Embryo import Embryo
from flask_restful import reqparse

''' 胚胎视图 '''

embryo_controller = Blueprint('embryo_controller', __name__)
url_prefix = '/front/embryo'

@embryo_controller.route('/', methods=['GET'])
@login_required
def main():
    logger().info('embryo_controller.embryo胚胎视图页面')

    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('embryoId', type=str)

    agrs = parser.parse_args()
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    embryoId = agrs['embryoId']
    return render_template('front/embryo/embryo.html', procedure_id=procedureId, dish_id=dishId, embryo_id=embryoId)