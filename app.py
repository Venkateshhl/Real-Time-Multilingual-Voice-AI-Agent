from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/health")
async def health():
    # Railway/Render healthchecks should not depend on external APIs.
    return {"status": "healthy"}

@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")

# Import and include the main WebSocket app
from backend.main import app as ws_app

# Mount the WebSocket routes
app.mount("/api", ws_app)