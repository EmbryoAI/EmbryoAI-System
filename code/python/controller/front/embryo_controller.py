from flask import Blueprint, jsonify,render_template
from common import logger
from app import login_required 
from entity.Embryo import Embryo

''' 胚胎视图 '''

embryo_controller = Blueprint('embryo_controller', __name__)
url_prefix = '/front/embryo'

@embryo_controller.route('/<string:id>/<string:dish_id>/<string:embryo_id>', methods=['GET'])
@login_required
def main(id, dish_id, embryo_id):
    logger().info('embryo_controller.embryo胚胎视图页面')
    return render_template('front/embryo/embryo.html', procedure_id=id, dish_id=dish_id, embryo_id=embryo_id)