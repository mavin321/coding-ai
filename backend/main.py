# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.ai import router as ai_router

app = FastAPI(title="AI Coding Assistant API")

# Allow React to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(ai_router, prefix="/api/ai")
