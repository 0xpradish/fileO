from fastapi import APIRouter, Depends, HTTPException
from boto3.dynamodb.conditions import Key


from ..dependencies import get_dynamodb_client, get_s3_client, BUCKET
from ..auth import get_current_user


router = APIRouter()


@router.delete("/delete/{docId}")
def delete_photo(docId: str, userId: str = Depends(get_current_user)):

    
    photos_table = get_dynamodb_client()
    s3_client =  get_s3_client()

    res = photos_table.query(
        KeyConditionExpression=Key("userId").eq(userId)
    )

    items = res["Items"]
    print(items)
    item = next((i for i in items if i["docId"] == docId), None)

    if not item:
        raise HTTPException(status_code=404, detail="Image not found")

    s3_key = item["s3Key"]

    s3_client.delete_object(
        Bucket=BUCKET,
        Key=s3_key
    )

    photos_table.delete_item(
        Key={
            "userId": userId,
            "uploadedAt": item["uploadedAt"]
        }
    )

    return {"status": "success", "deleted": docId}



