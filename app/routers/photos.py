
from fastapi import APIRouter, Depends
from boto3.dynamodb.conditions import Key

from ..dependencies import get_dynamodb_client
from ..auth import get_current_user



router = APIRouter()

@router.get("/photos")
def list_photos(userId: str = Depends(get_current_user)):


    doc_table = get_dynamodb_client()

    res = doc_table.query(
        KeyConditionExpression=Key("userId").eq(userId),
        ScanIndexForward=False )

    print(res["Items"])
    
    return res["Items"]