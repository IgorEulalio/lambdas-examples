import json
import mysql.connector
import csv
import boto3

# load environment variables
host = 'user-database.c9afqljva4w9.sa-east-1.rds.amazonaws.com'
user = 'admin'
password = 'k9sja2en'
database = 'Clients'
region = 'sa-east-1'

# establish mysql connection and s3 session
mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    csv_file = s3.get_object(Bucket=bucket, Key=key)
    csv_file_decoded = csv_file['Body'].read().decode('UTF-8').split('\n')
    users = get_users_csv(csv_file_decoded)

    insere_users(users)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }

def insere_users(users):
    mycursor = mydb.cursor()
    for user in users:
        print(user)
        sql = "INSERT INTO Clients (firstname, lastname, email) VALUES (%s, %s, %s)"
        val = (user["firstname"], user["lastname"], user["email"])
        mycursor.execute(sql, val)
        mydb.commit()

def get_users_csv(file_dir):
  with open(file_dir, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    users = []
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        firstname = row["firstname"]
        lastname = row["lastname"]
        email = row["email"]

        user = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        }
        
        users.append(user)
    return users