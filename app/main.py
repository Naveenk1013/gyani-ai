from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import logger
from .config import settings  # Import settings from config.py
from .ai import generate_response  # Import AI logic

# Create FastAPI instance
app = FastAPI()

# Add your Netlify frontend URL
frontend_url = "https://gyani-ai.netlify.app"

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # For local frontend testing
        "http://127.0.0.1:3000",
        frontend_url,   # Without trailing slash
        f"{frontend_url}/"  # With trailing slash
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Backend is running with CORS enabled!"}

# AI generation route
@app.get("/ai")
def get_ai_response(prompt: str, model: str = None):
    logger.info(f"AI request for prompt: {prompt[:50]}... with model: {model or 'default'}")
    try:
        response = generate_response(prompt, model)
        return {"response": response}
    except Exception as e:
        logger.error(f"AI generation failed: {str(e)}")
        return {"error": str(e)}