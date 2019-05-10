from flask import Blueprint, jsonify,render_template
import service.admin.user_service as user_service
from app import login_required 
import logUtils

''' 后台增删查改demo '''

user_controller = Blueprint('user_controller', __name__)
url_prefix = '/admin/user'

@user_controller.route('/', methods=['GET'])
@login_required
def main():
    logUtils.info('user_controller.main-跳转到后台管理的用户列表页面')
    return render_template('admin/user/user_manage.html',htmlType='user')

''' 跳转到添加页面 '''
@user_controller.route('/toAdd/', methods=['GET'])
@login_required
def toAdd():
    logUtils.info('user_controller.toAdd-跳转到后台管理的新增用户页面')
    return render_template('admin/user/add.html')

''' 跳转到用户编辑页面 '''
@user_controller.route('/edit/<string:id>', methods=['GET'])
@login_required
def edit(id):
    logUtils.info('user_controller.toAdd-跳转到后台管理的编辑用户页面')
    user = user_service.findUserById(id)
    return render_template('admin/user/edit.html', user=user)

''' 跳转到修改密码页面 '''
@user_controller.route('/toModifyPass', methods=['GET'])
@login_required
def toModifyPass():
    logUtils.info('user_controller.toAdd-跳转到后台管理的修改密码页面')
    return render_template('admin/user/toModifyPass.html')
