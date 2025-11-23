import boto3
import os
from dotenv import load_dotenv
from .config import is_local, AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY


load_dotenv()

BUCKET = str(os.getenv("BUCKET"))

def get_s3_client():
    if is_local():
        
        return boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )
    else:
        return boto3.client("s3", region_name=AWS_REGION)


def get_dynamodb_client():
    if is_local():
        dynamo = boto3.resource(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )
    else:
        dynamo = boto3.resource("dynamodb", region_name=AWS_REGION)

    return dynamo.Table("Documents")
