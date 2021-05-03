import json
import csv
import boto3

def lambda_handler(event, context):
    
    region = 'sa-east-1'
    record_list = []
    
    try:
        s3 = boto3.client('s3')
        
        dynamodb = boto3.client('dynamodb', region_name=region)
        
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print('Objeto: ' + key + " recebido no bucekt: " + bucket)
        
        csv_file = s3.get_object(Bucket=bucket, Key=key)
        
        record_list = csv_file['Body'].read().decode('UTF-8').split('\n')
        
        csv_reader = csv.reader(record_list, delimiter=';', quotechar='"')
        
        for row in csv_reader:
            stock_id = row[0]
            stock_name = row[1]
            stock_quotes = row[2]
            stock_value = row[3]
            print("Stock id: " + stock_id + " Stock name: " + stock_name + " Stock quote: " + stock_quotes + " Stock value: " + stock_value)
            
            add_to_db = dynamodb.put_item(
                TableName= 'stocks_table',
                Item= {
                    'stock_id' : {'S': str(stock_id)},
                    'stock_name' : {'S': str(stock_name)},
                    'stock_quotes' : {'N': str(stock_quotes)},
                    'stock_value' : {'S': str(stock_value)},
                })
                
            print('Sucessfuly added the records to the DynamoDB table')    
        
    except Exception as e:
        print(str(e))
    
    return {
        'statusCode': 200,
        'body': json.dumps('CSV to dynamoDB sucess!')
    }
