from flask import Blueprint, jsonify
from common import logger

test_controller = Blueprint('test_controller', __name__)
url_prefix = '/test'

@test_controller.route('/', methods=['GET'])
def test():
    logger().info('进入test_controller.test函数')
    return 'ok'