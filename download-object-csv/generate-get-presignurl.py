import json
import boto3
import os
from botocore.exceptions import ClientError

bucket = os.environ.get("S3_BUCKET_NAME")
region = os.environ.get("REGION")

s3 = boto3.client("s3", region_name=region)


def lambda_handler(event, context):

    object_key = event["queryStringParameters"]["file_key"]

    objet_from_s3 = getObject(object_key)
    
    print(object_key)
    print(bucket)
    print(region)
    
    return objet_from_s3
    
    
def getObject(object_key):
    try:
        return s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': object_key}, ExpiresIn = 15)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return "Objeto com a key: " + object_key + " nao encontrado"
            return dict()
    else:
        raise