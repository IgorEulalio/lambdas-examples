import boto3
import os

s3 = boto3.client("s3")
bucket = os.environ.get('S3_BUCKET_NAME')

def lambda_handler(event, context):
    
    object_names = []
    
    objects = s3.list_objects(Bucket=bucket)
    content = objects["Contents"]
    for obj in content:
        object_names.append(obj["Key"])
        print(obj)
    
    return object_names