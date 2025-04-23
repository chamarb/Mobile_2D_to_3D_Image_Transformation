from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from models.processing import process_image

router = APIRouter()

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Sauvegarde de l'image
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Traitement de l'image (Segmentation, Description, 3D Reconstruction)
        result = process_image(file_path)

        return {"message": "Image processed successfully!", "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")
