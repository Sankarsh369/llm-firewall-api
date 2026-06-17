import os
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
from app.nlp_engine import detector

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Initialize MongoDB Client (Falls back to local if .env isn't set yet)
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client["llm_firewall_db"]
logs_collection = db["attack_logs"]

class PromptRequest(BaseModel):
    prompt: str

class SecurityResponse(BaseModel):
    is_safe: bool
    threat_score: float
    flagged_patterns: list[str]

@router.post("/analyze", response_model=SecurityResponse, tags=["Security Engine"])
def analyze_prompt_endpoint(request: PromptRequest):
    """
    Receives a prompt, runs it through the engine, logs the transaction to MongoDB,
    and returns the security verdict.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="The prompt field cannot be empty.")
    
    # 1. Analyze the prompt using our NLP engine
    analysis_result = detector.analyze_prompt(request.prompt)
    
    # 2. Create a log payload to store in MongoDB
    log_payload = {
        "timestamp": datetime.utcnow(),
        "input_prompt": request.prompt,
        "is_safe": analysis_result["is_safe"],
        "threat_score": analysis_result["threat_score"],
        "flagged_patterns": analysis_result["flagged_patterns"]
    }
    
    # 3. Save silently to MongoDB Atlas
    try:
        logs_collection.insert_one(log_payload)
    except Exception as e:
        # We print the error to your terminal but don't crash the API response
        print(print(f"Database Logging Error: {e}"))

    return analysis_result