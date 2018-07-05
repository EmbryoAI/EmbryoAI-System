from flask import Blueprint, jsonify,render_template
from common import logger
import service.admin.incubator_service as incubator_service
from app import login_required 

''' 后台增删查改demo '''

admin_incubator_controller = Blueprint('admin_incubator_controller', __name__)
url_prefix = '/admin/incubator'

@admin_incubator_controller.route('/', methods=['GET'])
@login_required
def maim():
    logger().info('进入test1_controller.test函数')
    return render_template('admin/incubator/incubator.html',htmlType="incubator")

''' 跳转到添加页面 '''
@admin_incubator_controller.route('/toAdd/', methods=['GET'])
@login_required
def toAdd():
    return render_template('admin/incubator/add.html')

''' 跳转到用户详情页面 '''
@admin_incubator_controller.route('/toEdit/<string:id>', methods=['GET'])
@login_required
def detail(id):
    incubator = incubator_service.findIncubatorById(id)
    return render_template('admin/incubator/edit.html', incubator=incubator)