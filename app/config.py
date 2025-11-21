import os
from dotenv import load_dotenv

load_dotenv()

MODE = os.getenv("MODE", "local")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

def is_local():
    return MODE == "local"

def is_prod():
    return MODE == "prod"
