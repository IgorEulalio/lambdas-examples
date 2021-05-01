import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
bucket = os.environ.get("S3_BUCKET_NAME")


def lambda_handler(event, context):

    object_key = event["queryStringParameters"]["file_key"]

    objet_from_s3 = getObject(object_key)
    
    return objet_from_s3
    
    
def getObject(object_key):
    try:
        return s3.get_object(Bucket=bucket, Key=object_key)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return "Objeto com a key: " + object_key + " nao encontrado"
            return dict()
    else:
        raise
