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
    根据周期id、皿编码获取病历下的某个胚胎的最新时间序列下的缩略图
'''
@image_rest_controller.route('/findImageFouce', methods=['POST','GET'])
@login_required
def findImageFouce():
    parser = reqparse.RequestParser()
    parser.add_argument('procedureId', type=str)
    parser.add_argument('dishCode', type=str)
    imageData = image_service.getImageFouce(parser.parse_args())
    if imageData is not None:
        # print(1111111111111)
        # response = make_response(imageData)
        # response.headers['Content-Type'] = 'image/png'
        # return response
        return imageData
    else :
        return ""


''' 
    查询最新的采集目录下的培养箱里的三个皿里的12张缩略图
'''
@image_rest_controller.route('/findNewestImageUrl', methods=['POST','GET'])
def findNewestImageUrl():
    parser = reqparse.RequestParser()
    parser.add_argument('pageNo', type=int)
    parser.add_argument('pageSize', type=int)
    # code, imageUrlList = image_service.findNewestImageUrl(parser.parse_args())
    # return make_response(jsonify(imageUrlList), code)
    imageUrlList = image_service.findNewestImageUrl(parser.parse_args())
    return jsonify(imageUrlList.__dict__)