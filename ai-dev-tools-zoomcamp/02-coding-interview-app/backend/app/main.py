from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sessions, websocket, execution

app = FastAPI(title="Coding Interview App")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router)
app.include_router(websocket.router)
app.include_router(execution.router)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ... (existing code)

app.include_router(sessions.router)
app.include_router(websocket.router)
app.include_router(execution.router)

# Serve Frontend Static Files
# We expect the frontend build to be in ../frontend/dist (relative to backend/app/main.py? No, relative to CWD)
# In Docker, we will copy dist to /app/frontend/dist or similar.
# Let's assume a standard path structure for Docker: /app/static
# But for local dev? Local dev uses `npm run dev` and `uvicorn` separately.
# So this static serving is primarily for the Docker production build.
# We can check if the directory exists.

frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # If API route, it would have been caught above (FastAPI matches in order? No, specific routes first usually)
        # But we mounted routers first.
        # However, catch-all might shadow if not careful.
        # Actually, `mount` matches path prefixes.
        # We want to serve index.html for any non-API route.
        
        # Check if file exists in dist (e.g. favicon.ico)
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Otherwise return index.html
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Coding Interview App Backend (Frontend not built)"}
