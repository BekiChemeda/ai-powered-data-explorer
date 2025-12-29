from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, analysis, ai, settings, files
from app.database import engine, Base
import os

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Data Explorer", description="Self-hosted AI-powered Data Exploration Tool")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(ai.router, prefix="/api", tags=["AI"])
app.include_router(settings.router, prefix="/api", tags=["Settings"])
app.include_router(files.router, prefix="/api", tags=["Files"])

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/upload")
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/my-files")
async def my_files_page(request: Request):
    return templates.TemplateResponse("my_files.html", {"request": request})

@app.get("/settings")
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/results")
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})
