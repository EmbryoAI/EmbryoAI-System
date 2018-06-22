from flask import Blueprint, jsonify,render_template
from common import logger
import service.admin.user_service as user_service

''' 后台增删查改demo '''

user_controller = Blueprint('user_controller', __name__)
url_prefix = '/admin/user'

@user_controller.route('/', methods=['GET'])
def main():
    return render_template('admin/user/user_manage.html')


''' 跳转到添加页面 '''
@user_controller.route('/toAdd/', methods=['GET'])
def toAdd():
    return render_template('admin/user/add.html')

''' 跳转到用户详情页面 '''
@user_controller.route('/detail/<string:id>', methods=['GET'])
def detail(id):
    user = user_service.findUserById(id)
    return render_template('admin/user/detail.html', user=user)

