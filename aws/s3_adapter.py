import boto3

aws_access_key = "ASIAXPWA7CPLVIA5BSNI"
aws_secret_key = "cawKrL7FrWw/MR2k5LlB2q1HBS2mVmIld27Pnq9g"
aws_session_token = "FwoGZXIvYXdzEPz//////////wEaDOabvZUUM54geCMIGiLLAWv320101IhHihs7dRyAgG5w5D5tWhB+QW3KBE89qWrJ2Labh0gjMOc04sejHtbF7aki8N9hrOvxk3P4StaSGoK/+5yf6ghnBLSk+JUQ1y8EbdLJE2AnzgVvK5CGNIcCJVcbp1DPOBdOJ56yrD7oBNdDZ88ZfRTrijHemi+AukvffvrzBEPZ0DZ35CspTuhCbxZZwkLAX9oVYylnYUs64ldGmUkFHQ2zHsqxi4TvW+eM0E+qn3gI/cmL/RumAf8BIv/H1xaAUEyRm+PRKMzVi40GMi28V1xkTQKI+7H/N53ZjYCcI/cCxsftpqbqDQKuj6WEHA/lI4NMGw+Dopm659E="

s3 = boto3.resource(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    aws_session_token=aws_session_token
)
bucket_name = 'filetransformer'


def download_file(file_name):
    path_bucket = '{0}/{1}'.format('input', file_name)
    s3.meta.client.download_file(
        bucket_name,
        path_bucket,
        file_name
    )


def upload_file(file_name):
    path_bucket = '{0}/{1}'.format('output', file_name)
    s3.meta.client.upload_file(file_name, bucket_name, path_bucket)


def delete_file(file_name):
    s3.meta.client.delete_object(
        Bucket=bucket_name,
        Key=file_name
    )
