
from fastapi import APIRouter, Depends, HTTPException

from boto3.dynamodb.conditions import Key
from ..dependencies import get_dynamodb_client

from ..auth import get_current_user

router = APIRouter()



@router.get("/photos")
def list_photos(userId: str = Depends(get_current_user)):


    photos_table = get_dynamodb_client()

    res = photos_table.query(
        KeyConditionExpression=Key("userId").eq(userId),
        ScanIndexForward=False )

    print(res["Items"])
    
    return res["Items"]