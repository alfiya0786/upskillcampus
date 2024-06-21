import boto3

s3_client = boto3.client('s3')
s3_client.create_bucket(Bucket='my-healthcare-data', CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
