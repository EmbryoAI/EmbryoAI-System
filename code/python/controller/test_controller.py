from flask import Blueprint, jsonify, request
from common import logger
from flask import Flask, request, render_template
test_controller = Blueprint('test_controller', __name__,template_folder='templates1')
url_prefix = '/test'

@test_controller.route('/', methods=['GET'])
def test():
    logger().info('进入test_controller.test函数')
    return render_template('test/home.html')

@test_controller.route('/abc', methods=['POST'])
def abc():
    code = request.json.get('code')
    print(code)
    return jsonify({'code': code})
 