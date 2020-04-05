# -*- coding: utf8 -*-

from task.TimeSeries import TimeSeries, serie_to_minute
from task.process_dish_dir import dir_filter
from task.dish_config import SerieInfo
import os
import json
from app import app, conf, minioClient, organizationId
from common import getdefault
from service.front.organization_service import getOrganConfig
from minio import Minio
from minio.error import ResponseError
import logUtils as logger  # 日志


def upload_dish(path, dish_info, air):
    """
    处理一个皿目录方法
        @param path: 采集目录完整路径
        @param dish_info: DishConfig配置信息对象
        @returns state: 皿结束采集标志 True - 已结束采集；False - 未结束采集
    """
    init_minio()
    if minioClient is None or organizationId is None:
        logger.error("上传图像失败，机构ID为空")
        return False
    from functools import partial

    dish_path = path + f"DISH{dish_info.index}" + os.path.sep  # 皿目录完整路径
    last_op = "0" * 7
    processed = TimeSeries().range(last_op)
    # 以下两行代码使用偏函数从当前目录中得到所有合法且未处理的时间序列子目录
    f = partial(dir_filter, processed=processed, base=dish_path)
    todo = list(sorted(filter(f, os.listdir(dish_path))))
    logger.debug(f"需要上传图片的目录：{todo}")

    isConplete = True
    for serie in todo:
        # 交给process_serie_dir模块对时间序列目录进行处理
        flag = upload_serie(dish_path, air, serie, dish_info)
        # 每次处理完成都将最新处理的时间序列目录回写到state对象中
        isConplete = isConplete & flag
    # 返回皿目录是否已经结束采集的标志
    return isConplete


def upload_serie(dish_path, air, serie, dish_info):
    """
    上传某一时间序列下所有孔最清晰的图
        @param dish_path: 采集目录的完整路径，为了读取DishInfo.ini文件
        @param air : 采集目录
        @param serie: 最后处理完成的时间序列目录名称
        @param dish_info: DishConfig配置信息对象
        @returns state: True - 结束采集；False - 未结束采集
    """
    serie_path = dish_path + serie + os.path.sep  # 时间序列目录完整路径
    wells = dish_info.wells  # 皿中所有的孔信息
    flag = True
    for c in wells:
        logger.debug(f"上传 序列 {serie} 孔 {wells[c].index} 中最清晰的图")
        serie_info = SerieInfo()
        serie_info.serieSetup(wells[c], serie)
        sharpestJpgName = serie_info.sharp
        objNmae = (
            air
            + "/"
            + str(dish_info.index)
            + "/"
            + str(wells[c].index)
            + "/"
            + serie
            + "/"
            + sharpestJpgName
        )
        # conf['STATIC_NGINX_IMAGE_URL'] + os.path.sep
        url = serie_path + sharpestJpgName
        flag = flag & upload_image(objNmae, url)
    return flag


def upload_image(name, url):
    try:
        if os.path.exists(url):
            etag = minioClient.fput_object(
                organizationId, name, url, content_type="application/x-jpg"
            )
            if etag is None:
                logger.error("上传图像失败，机构id：" + organizationId + ",路径：" + url)
                return False
            else:
                logger.debug("上传图像成功，机构id：" + organizationId + "路径：" + url)
                return True
        else:
            logger.debug(f"{url}文件不存在，不做上传")
            return True
    except ResponseError as err:
        logger.error("上传图像失败，机构id：" + organizationId + ",路径：" + url)
        logger.error(err)
        return False


def init_minio():
    global minioClient, organizationId
    try:
        if minioClient is None or organizationId is None:
            org = getOrganConfig()
            if org is None:
                logger.error("机构未注册到云端，未获取到机构ID及minio用户账号，不上传图像。")
            else:
                logger.info("获取到机构ID及minio用户账号，初始化minio客户端。")
                organizationId = org["orgId"]
                # 使用endpoint、access key和secret key来初始化minioClient对象。
                minioClient = Minio(
                    conf["MINIO_IP_PORT"],
                    access_key=org["s3Username"],
                    secret_key=org["s3Password"],
                    secure=False,
                )

                # minioClient = Minio(conf["MINIO_IP_PORT"],
                #             access_key='UV1NSZLV9V9IKT5KAPJX',
                #             secret_key='DuiZ4PTm5L+3LHt+aRyxblWk7fW6Hv2nsKtIJNal',
                #             secure=False)
                if minioClient.bucket_exists(organizationId) is False:
                    minioClient.make_bucket(organizationId)
    except ResponseError as err:
        logger.error(f"初始化monio客户端失败：{err}")
