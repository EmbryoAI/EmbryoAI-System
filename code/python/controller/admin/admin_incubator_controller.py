from flask import Blueprint, render_template
import logUtils
import service.admin.incubator_service as incubator_service
from app import login_required

''' 后台增删查改demo '''

admin_incubator_controller = Blueprint('admin_incubator_controller', __name__)
url_prefix = '/admin/incubator'

'''培养箱列表'''
@admin_incubator_controller.route('/', methods=['GET'])
@login_required
def maim():
    logUtils.info('admin_incubator_controller.maim-跳转到培养箱列表界面')
    return render_template('admin/incubator/incubator.html', htmlType="incubator")

''' 跳转到添加页面 '''
@admin_incubator_controller.route('/toAdd/', methods=['GET'])
@login_required
def toAdd():
    logUtils.info('admin_incubator_controller.toAdd-跳转到新增培养箱界面')
    return render_template('admin/incubator/add.html')

''' 跳转到培养箱编辑页面 '''
@admin_incubator_controller.route('/toEdit/<string:id>', methods=['GET'])
@login_required
def detail(id):
    logUtils.info('admin_incubator_controller.detail-跳转到培养箱编辑页面')
    incubator = incubator_service.findIncubatorById(id)
    return render_template('admin/incubator/edit.html', incubator=incubator)