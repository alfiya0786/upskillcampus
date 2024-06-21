import json
import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
rds = boto3.client('rds-data')
secrets_manager = boto3.client('secretsmanager')

def handler(event, context):
    bucket_name = os.environ['S3_BUCKET']
    db_secret_arn = os.environ['DB_SECRET']
    
    try:
        if event['httpMethod'] == 'POST':
            # Process POST request
            body = json.loads(event['body'])
            patient_id = body['patient_id']
            data = body['data']
            
            # Store data in S3
            s3.put_object(Bucket=bucket_name, Key=f'{patient_id}.json', Body=json.dumps(data))
            
            # Insert metadata into RDS
            secret_response = secrets_manager.get_secret_value(SecretId=db_secret_arn)
            secret_string = json.loads(secret_response['SecretString'])
            username = secret_string['username']
            password = secret_string['password']
            db_cluster_arn = os.environ['DB_CLUSTER_ARN']
            db_name = os.environ['DB_NAME']
            
            sql = f"INSERT INTO patients (patient_id, data) VALUES (:patient_id, :data)"
            rds.execute_statement(
                resourceArn=db_cluster_arn,
                secretArn=db_secret_arn,
                database=db_name,
                sql=sql,
                parameters=[
                    {'name': 'patient_id', 'value': {'stringValue': patient_id}},
                    {'name': 'data', 'value': {'stringValue': json.dumps(data)}}
                ]
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps('Data stored successfully!')
            }
        
        elif event['httpMethod'] == 'GET':
            # Process GET request
            patient_id = event['queryStringParameters']['patient_id']
            
            # Retrieve data from S3
            s3_response = s3.get_object(Bucket=bucket_name, Key=f'{patient_id}.json')
            data = s3_response['Body'].read().decode('utf-8')
            
            return {
                'statusCode': 200,
                'body': data
            }
        
        else:
            return {
                'statusCode': 405,
                'body': json.dumps('Method Not Allowed')
            }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {e}")
        }
