import os
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as firewall_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LLM Firewall API",
    description="An AI security endpoint to detect and block prompt injection attacks.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read the secret key from environment variables
EXPECTED_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET")

async def verify_rapidapi_secret(x_rapidapi_proxy_secret: str = Header(None)):
    """
    Security gatekeeper: Ensures requests are routed securely through RapidAPI proxy.
    Allows local development testing if no secret key is set in .env yet.
    """
    if EXPECTED_SECRET and x_rapidapi_proxy_secret != EXPECTED_SECRET:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized access. This API must be accessed via the official RapidAPI marketplace."
        )

# Protect all routes under /api/v1 with our verification dependency
app.include_router(
    firewall_router, 
    prefix="/api/v1", 
    dependencies=[Depends(verify_rapidapi_secret)]
)

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "message": "LLM Firewall API proxy gate is active."
    }