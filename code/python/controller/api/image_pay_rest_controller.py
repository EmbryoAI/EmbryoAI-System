from flask import Blueprint, jsonify, request, make_response, Response
from flask_restful import reqparse
import service.front.image_pay_service as image_pay_service
import logUtils

image_pay_rest_controller = Blueprint("image_pay_rest_controller", __name__)
url_prefix = "/api/v1/image/pay"

""" 根据周期id、皿ID、孔ID、获取孔的时间序列对应最清晰的URL
    @param procedureId: 周期id
    @param dishId ： 皿id
    @param wellId ： 孔编号
"""


@image_pay_rest_controller.route("/queryClearImageUrl", methods=["POST", "GET"])
def queryClearImageUrl():
    logUtils.info(
        "feedback_rest_controller.queryClearImageUrl-根据周期id、皿ID、孔ID、获取孔的时间序列对应最清晰的URL"
    )
    parser = reqparse.RequestParser()
    parser.add_argument("procedureId", type=str)
    parser.add_argument("dishId", type=str)
    parser.add_argument("wellId", type=str)
    code, clearImageUrlList = image_pay_service.queryClearImageUrl(parser.parse_args())
    return make_response(jsonify(clearImageUrlList), code)


""" 根据周期id、皿ID、孔ID、获取孔的时间序列对应缩略图的URL
    @param procedureId: 周期id
    @param dishId ： 皿id
    @param wellId ： 孔编号
"""


@image_pay_rest_controller.route("/queryThumbnailImageUrl", methods=["POST", "GET"])
def queryThumbnailImageUrl():
    logUtils.info(
        "image_pay_rest_controller.queryThumbnailImageUrl-根据周期id、皿ID、孔ID、获取孔的时间序列对应缩略图的URL"
    )
    parser = reqparse.RequestParser()
    parser.add_argument("procedureId", type=str)
    parser.add_argument("dishId", type=str)
    parser.add_argument("wellId", type=str)
    code, thumbnailImageUrlList = image_pay_service.queryThumbnailImageUrl(
        parser.parse_args()
    )
    return make_response(jsonify(thumbnailImageUrlList), code)
