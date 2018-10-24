from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 
from entity.Embryo import Embryo
from flask_restful import reqparse
import service.front.embryo_service as embryo_service

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
    parser.add_argument('cellCode', type=str)

    agrs = parser.parse_args()
    procedureId = agrs['procedureId']
    dishId = agrs['dishId']
    embryoId = agrs['embryoId']
    cellCode = agrs['cellCode']
    return render_template('front/embryo/embryo.html', procedure_id=procedureId, dish_id=dishId, embryo_id=embryoId, cell_code=cellCode)

@embryo_controller.route('/toEmbryo', methods=['GET'])
@login_required
def toEmbryo():
    logger().info('embryo_controller.toEmbryo胚胎视图页面')

    parser = reqparse.RequestParser()
    parser.add_argument('imagePath', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellCode', type=str)
    
    procedureId,dishId,embryoId = embryo_service.findEmbroyoInfo(parser.parse_args())
    return render_template('front/embryo/embryo.html', procedure_id=procedureId, dish_id=dishId, embryo_id=embryoId)