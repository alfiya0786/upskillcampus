import boto3

ec2_client = boto3.client('ec2')
response = ec2_client.run_instances(
    ImageId='ami-0abcdef1234567890',
    InstanceType='t2.micro',
    KeyName='Datamanage',
    SecurityGroupIds=['sg-0603fbe43075c6a97'],
    SubnetId='subnet-07dc70b5940aa4615',
    MinCount=1,
    MaxCount=1
)
instance_id = response['Instances'][0]['InstanceId']
