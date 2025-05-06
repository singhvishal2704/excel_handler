import boto3
import os
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "ap-south-1")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)

def upload_to_s3(file_obj, s3_key):
    try:
        s3_client.upload_fileobj(file_obj, AWS_STORAGE_BUCKET_NAME, s3_key)
        return f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    except ClientError as e:
        raise Exception(f"S3 Upload Failed: {e}")


def download_from_s3(s3_key):
    try:
        file_obj = s3_client.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
        return file_obj['Body'].read()
    except ClientError as e:
        raise Exception(f"S3 Download Failed: {e}")

