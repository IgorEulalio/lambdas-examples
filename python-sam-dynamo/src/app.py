import json
import boto3
from botocore.exceptions import ClientError

# client = boto3.resource('dynamodb', endpoint_url="http://docker.for.mac.localhost:8000", region_name='sa-east-1')
client = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    received_ip = event["headers"]["X-Forwarded-For"]
    print("iniciando lambda..")
    item = get_item_dynamo()

    print("received ip: " + str(received_ip))

    print(item)

    album_title = item["Item"]["AlbumTitle"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "bem vindo victor",
            "ip": str(received_ip)
        }),
    }

def get_item_dynamo():

    print('buscando na table: ')
    table = client.Table('Music')
    try:
        response = table.get_item(Key={'Artist' :'Acme Band' ,'SongTitle' : 'Happy Day'})
    except ClientError as e:
        print("Error" + str(e.response['Error']['Message']))
    else:
        return response