from flask import Blueprint, jsonify,request, make_response,Response
from flask_restful import reqparse
import service.front.image_service as image_service
from common import logger

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

@image_rest_controller.route('/findAllZIndex', methods=['POST','GET'])
def findAllZIndex():
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishId', type=str)
    parser.add_argument('wellId', type=str)
    parser.add_argument('timeSeries', type=str)

    return image_service.getAllZIndex(parser.parse_args())