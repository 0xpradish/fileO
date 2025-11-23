from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.routers import delete
from app.routers import photos
from app.routers import upload
from app.routers import login

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(delete.router)
app.include_router(photos.router)
app.include_router(upload.router)
app.include_router(login.router)



@app.route("/")
def main():
    return {"message": "fileO API is running"}



handler = Mangum(app)