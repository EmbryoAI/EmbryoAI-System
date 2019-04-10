from flask import Blueprint, jsonify,request, make_response,Response
from flask_restful import reqparse
import service.front.image_service as image_service
from common import logger
from app import login_required

image_rest_controller = Blueprint('image_rest_controller', __name__)
url_prefix = '/api/v1/image'

''' 根据周期id、皿编号、孔编号、时间序列、z轴位置获取图像
    @param procedureId: 周期id
    @param dishId ： 皿id
    @param wellId ： 孔编号
    @param timeSeries ： 时间序列
    @param zIndex ： z轴位置
'''
@image_rest_controller.route('/findImage', methods=['POST','GET'])
@login_required
def findImage():
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellId', type=str)
    parser.add_argument('timeSeries', type=str)
    parser.add_argument('zIndex',type=str)
    imageData = image_service.getImageByCondition(parser.parse_args())
    if imageData :
        response = make_response(imageData)
        response.headers['Content-Type'] = 'image/png'
    return response

''' 根据周期id、皿编号、孔编号、时间序列获取z轴数据
    @param procedureId: 周期id
    @param dishId ： 皿id
    @param wellId ： 孔编号
    @param timeSeries ： 时间序列
'''
@image_rest_controller.route('/findAllZIndex', methods=['POST','GET'])
@login_required
def findAllZIndex():
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellId', type=str)
    parser.add_argument('timeSeries', type=str)

    return image_service.getAllZIndex(parser.parse_args())

@image_rest_controller.route('/markDistinct', methods=['POST'])
@login_required
def markDistinct():
    parser = reqparse.RequestParser()
    parser.add_argument('path', type=str)
    parser.add_argument('imageName', type=str)
    parser.add_argument('timeSeries', type=str)
    parser.add_argument('wellId', type=str)

    return image_service.markDistinct(parser.parse_args())




''' 
    查询最新的采集目录下的三个皿里的12张缩略图
'''
@image_rest_controller.route('/findNewestImageUrl', methods=['POST','GET'])
def findNewestImageUrl():
    imageUrlList = image_service.findNewestImageUrl()
    return jsonify(imageUrlList.__dict__)


''' 根据周期id、皿编号、孔编号、时间序列、z轴位置获取图像路径
    @param procedureId: 周期id
    @param dishId ： 皿id
    @param wellId ： 孔编号
    @param timeSeries ： 时间序列
    @param zIndex ： z轴位置
'''
@image_rest_controller.route('/getBigImagePath', methods=['POST','GET'])
@login_required
def getBigImagePath():
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellId', type=str)
    parser.add_argument('timeSeries', type=str)
    parser.add_argument('zIndex',type=str)
    imageUrl = image_service.getBigImagePath(parser.parse_args())
    return jsonify(imageUrl.__dict__)