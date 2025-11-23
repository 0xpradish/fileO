from fastapi import APIRouter, Depends
import uuid
import time
from pydantic import BaseModel
from typing import List, Dict

from ..dependencies import get_dynamodb_client, get_s3_client, BUCKET
from ..auth import get_current_user

router = APIRouter()


class FileInfo(BaseModel):
    name: str
    type: str  

class PresignRequest(BaseModel):
    files: list[FileInfo]
        

class PresignedPost(BaseModel):
    url: str                
    fields: Dict[str, str]  

class PresignResponse(BaseModel):
    uploadUrls: List[PresignedPost]   
    keys: List[str]                  


@router.post("/upload", response_model=PresignResponse)
def generate_presigned_urls(req: PresignRequest, userId: str = Depends(get_current_user)):

    urls = []
    keys = []

    for file in req.files:     
        original_name = file.name.lower()
        mime = file.type or ""

        if mime.startswith("image/") or original_name.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            fileType = "image"
            ext = original_name.split(".")[-1]
            if ext == original_name: 
                ext = "jpg"
            mime = mime or "image/jpeg"

        elif mime.startswith("video/") or original_name.endswith((".mp4", ".mov", ".avi", ".webm", ".mkv")):
            fileType = "video"
            ext = original_name.split(".")[-1]
            if ext == original_name:
                ext = "mp4"
            mime = mime or "video/mp4"

        else:
            
            fileType = "document"

            
            if "." in original_name:
                ext = original_name.split(".")[-1]
            else:
                ext = "bin"

            mime = mime or "application/octet-stream"

        
        docId = str(uuid.uuid4())
        key = f"uploads/{docId}.{ext}"

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
                "docId": docId,
                "s3Key": key,
                "mimeType": mime,
                "fileType": fileType
            }
        )

        urls.append(PresignedPost(url=presigned["url"], fields=presigned["fields"]))
        keys.append(key)

    return PresignResponse(uploadUrls=urls, keys=keys)

