
# 引入Minio包。
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

# 使用endpoint、access key和secret key来初始化minioClient对象。
minioClient = Minio('39.104.173.18:9000',
                    access_key='UV1NSZLV9V9IKT5KAPJX',
                    secret_key='DuiZ4PTm5L+3LHt+aRyxblWk7fW6Hv2nsKtIJNal',
                    secure=False)

# 调用make_bucket来创建一个存储桶。
try:
        print(minioClient.bucket_exists("testimages"))
        if minioClient.bucket_exists("testimages") is False :
                minioClient.make_bucket("testimages")
        
        buckets = minioClient.list_buckets()
        for bucket in buckets:
                print(bucket.name, bucket.creation_date)
    
    
except BucketAlreadyOwnedByYou as err:
       pass
except BucketAlreadyExists as err:
       pass
except ResponseError as err:
        raise
else:
        pass