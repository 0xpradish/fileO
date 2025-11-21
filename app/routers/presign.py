from fastapi import APIRouter, Depends, HTTPException
import uuid
import time

from pydantic import BaseModel
from typing import List, Dict

from ..dependencies import get_dynamodb_client, get_s3_client, BUCKET

from ..auth import get_current_user

router = APIRouter()




class PresignRequest(BaseModel):
    count: int              
    fileType: str           

class PresignedPost(BaseModel):
    url: str                
    fields: Dict[str, str]  

class PresignResponse(BaseModel):
    uploadUrls: List[PresignedPost]   
    keys: List[str]                  


@router.post("/presign-batch", response_model=PresignResponse)
def generate_presigned_urls(req: PresignRequest,userId: str = Depends(get_current_user)):
    

    urls = []
    keys = []

    if req.fileType == "image":
        mime = "image/jpeg"
        ext = "jpg"
    else:
        mime = "video/mp4"
        ext = "mp4"


    for _ in range(req.count):
        imageId = str(uuid.uuid4())
        key = f"uploads/{imageId}.{ext}"

        

        s3_client = get_s3_client()
        presigned = s3_client.generate_presigned_post(
            Bucket=BUCKET,
            Key=key,
            Fields={"Content-Type": mime},
            Conditions=[{"Content-Type": mime}],
            ExpiresIn=3600
        )

        presigned["url"] = f"https://{BUCKET}.s3.ap-south-1.amazonaws.com"


        photos_table = get_dynamodb_client()

        photos_table.put_item(
            Item={
                "userId": userId,
                "uploadedAt": int(time.time() * 1000),   
                "imageId": imageId,
                "s3Key": key,
                "mimeType": mime
            }
        )

        urls.append(PresignedPost(url=presigned["url"], fields=presigned["fields"]))
        keys.append(key)

    return PresignResponse(uploadUrls=urls, keys=keys)
