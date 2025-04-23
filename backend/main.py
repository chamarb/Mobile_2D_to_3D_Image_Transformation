from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from routes.image_processing import router as image_processing_router

app = FastAPI(
    title="Mon API",
    description="API pour la gestion des fichiers et la visualisation 3D",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossiers statiques
static_dir = os.path.join(os.path.dirname(__file__), "static")
uploads_dir = os.path.join(static_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/3d_viewer", StaticFiles(directory="static/3d_viewer"), name="3d_viewer")

# Endpoint de test
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Backend FastAPI is running!"}

# Serve un fichier 3D
@app.get("/static/uploads/{file_name}", response_class=FileResponse, tags=["Files"])
async def serve_model(file_name: str):
    file_path = os.path.join(uploads_dir, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    return FileResponse(file_path, media_type="application/octet-stream")

# ✅ Ajoute le router
app.include_router(image_processing_router)
