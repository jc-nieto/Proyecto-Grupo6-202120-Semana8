import boto3
from config import AWS_SESSION_TOKEN, AWS_SECRET_KEY, AWS_ACCESS_KEY, S3_BUCKET_NAME


bucket_name = S3_BUCKET_NAME

s3 = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)


def download_file(file_name, path):
    path_bucket = '{0}/{1}'.format('input', file_name)
    s3.meta.client.download_file(
        bucket_name,
        path_bucket,
        path
    )


def upload_file(file_name, path):
    path_bucket = '{0}/{1}'.format('output', file_name)
    s3.meta.client.upload_file(path, bucket_name, path_bucket)


def delete_file(file_name):
    s3.meta.client.delete_object(
        Bucket=bucket_name,
        Key=file_name
    )
