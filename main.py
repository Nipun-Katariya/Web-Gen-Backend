from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import os
import shutil

local_url = "http://localhost:3000"
vercel_url = "https://web-gen-frontend-seven.vercel.app"

app = FastAPI()

UPLOAD_DIR = "uploaded_files"  # or any suitable directory

# Root URL
@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[local_url, vercel_url],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route to upload and extract files
@app.post("/upload-flask-app/")
async def upload_flask_app(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(file_location, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_DIR)

    return {"filename": file.filename, "message": "File uploaded and extracted successfully!"}

# Route to delete all files
@app.delete("/delete-files/")
async def delete_files():
    if os.path.exists(UPLOAD_DIR):
        shutil.rmtree(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR, exist_ok=True)  # Recreate the directory after deletion
    return {"message": "All files deleted successfully!"}

# Vercel expects this format for ASGI apps
app = app
