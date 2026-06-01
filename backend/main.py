from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from models.user import User
from models.candidate_set import CandidateSetResponse
from pipeline.main_pipeline import run_pipeline

load_dotenv()

app = FastAPI(title="BRAHMO Rules Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

class PipelineRequest(BaseModel):
    user_id: str

@app.get("/users")
def get_users():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    res = supabase.table("users").select("*").execute()
    return res.data

@app.post("/pipeline", response_model=CandidateSetResponse)
def execute_pipeline(req: PipelineRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
        
    # Get user
    res = supabase.table("users").select("*").eq("id", req.user_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = User(**res.data[0])
    
    # Run pipeline
    result = run_pipeline(user, supabase)
    return result
