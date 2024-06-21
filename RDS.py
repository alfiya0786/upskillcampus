import boto3

rds_client = boto3.client('rds')
rds_client.create_db_instance(
    DBInstanceIdentifier='mydbinstance',
    AllocatedStorage=20,
    DBInstanceClass='db.t2.micro',
    Engine='mysql',
    Username='admin',
    UserPassword='Ask1234',
    BackupRetentionPeriod=7
)
