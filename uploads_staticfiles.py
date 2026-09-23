from fastapi import FastAPI,HTTPException,UploadFile,File
from fastapi.staticfiles import StaticFiles
import os
import shutil 

app = FastAPI()

# make the upload folder

UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Statci File setup

app.mount("/files",StaticFiles(directory=UPLOADS_DIR),name="files")

# Upload file's api

@app.post("/uploads")
def uploads(file:UploadFile=File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOADS_DIR,filename)
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not selected"
        )
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    return{
        "Message":"File Uploaded Successfully",
        "filename":filename,
        "File_path":f"http://127.0.0.1:8000/files/{filename}"
    }

# get the uploaded files
@app.get("/file/{filename}")
def get_file(filename:str):
    file_path = os.path.join(UPLOADS_DIR,filename)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File path Incorrect"
        )
    return{
        "file_path":f"http://127.0.0.1:8000/files/{filename}"
    }