from flask import Blueprint, render_template
import logUtils

admin_index_controller = Blueprint('admin_index_controller', __name__)
url_prefix = '/admin/index'

@admin_index_controller.route('/', methods=['GET'])
def index():
    logUtils.info('admin_index_controller.index-跳转到后台管理首页')
    return render_template('admin/main.html')

@admin_index_controller.route('/login', methods=['GET'])
def toLogin():
    logUtils.info('admin_index_controller.index-进入后台管理login页面')
    return render_template('login.html')





