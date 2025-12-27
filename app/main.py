from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import data_router
import os

app = FastAPI(title="AI-Powered Data Exploration App")

# Include routers
app.include_router(data_router.router, prefix="/api")

# Mount static files for frontend
# Ensure the directory exists
if not os.path.exists("app/frontend"):
    os.makedirs("app/frontend")

app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("app/frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
