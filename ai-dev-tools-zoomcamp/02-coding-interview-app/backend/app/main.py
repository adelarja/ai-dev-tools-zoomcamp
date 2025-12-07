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

@app.get("/")
async def root():
    return {"message": "Coding Interview App Backend"}
