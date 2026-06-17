from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# We will import our NLP detection routes here later
from app.routes import router as firewall_router

app = FastAPI(
    title="LLM Firewall API",
    description="An AI security endpoint to detect and block prompt injection attacks.",
    version="1.0.0"
)

# Set up CORS (Cross-Origin Resource Sharing)
# This allows external developer applications to ping your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# We will activate this once we build the routes.py file
app.include_router(firewall_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "message": "LLM Firewall API is active and listening.",
        "docs_url": "Navigate to http://127.0.0.1:8000/docs to view the interactive API documentation."
    }