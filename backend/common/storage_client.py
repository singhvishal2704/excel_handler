import os
from uuid import uuid4
from botocore.exceptions import ClientError
from common.logging_utils import logger

USE_S3 = os.getenv("ENV", "dev") == "prod"

if USE_S3:
    import boto3
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

    def upload_file(file_obj, filename):
        try:
            s3_key = f"uploads/{uuid4()}_{filename}"
            s3_client.upload_fileobj(file_obj, AWS_STORAGE_BUCKET_NAME, s3_key)
            return f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{s3_key}"
        except ClientError as e:
            logger.exception("S3 Upload Failed")
            raise Exception(f"S3 Upload Failed: {e}")

    def download_file(s3_key):
        try:
            file_obj = s3_client.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
            return file_obj['Body'].read()
        except ClientError as e:
            logger.exception("S3 Download Failed")
            raise Exception(f"S3 Download Failed: {e}")

else:
    LOCAL_UPLOAD_DIR = os.path.join("media", "temp_uploaded_files")
    os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

    def upload_file(file_obj, filename):
        try:
            filepath = os.path.join(LOCAL_UPLOAD_DIR, f"{uuid4()}_{filename}")
            with open(filepath, "wb") as f:
                f.write(file_obj.read())
            return filepath
        except Exception as e:
            logger.exception("Local Upload Failed")
            raise Exception(f"Local Upload Failed: {e}")

    def download_file(filepath):
        try:
            with open(filepath, "rb") as f:
                return f.read()
        except Exception as e:
            logger.exception("Local Download Failed")
            raise Exception(f"Local Download Failed: {e}")
