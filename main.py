from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import del_photos
from app.routers import photos
from app.routers import presign
from app.routers import login

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(del_photos.router)
app.include_router(photos.router)
app.include_router(presign.router)
app.include_router(login.router)




@app.route("/")
def main():
    return {"message": "fileO API is running"}



handler = Mangum(app)