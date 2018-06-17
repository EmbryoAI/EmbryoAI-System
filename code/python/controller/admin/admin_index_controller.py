from flask import Blueprint, jsonify,render_template
from common import logger

admin_index_controller = Blueprint('admin_index_controller', __name__)
url_prefix = '/admin/index'

@admin_index_controller.route('/', methods=['GET'])
def test():
    logger().info('进入test1_controller.test函数')
    return render_template('admin/main.html')

@admin_index_controller.route('/login', methods=['GET'])
def index():
    logger().info('进入login页面')
    return render_template('login.html')





