from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from database.database import get_db, engine
from database.models import Base
from routers import auth, career_prediction, github_analysis, skill_gap, roadmap
from ml_models.career_classifier import CareerClassifier
from ml_models.salary_predictor import SalaryPredictor

load_dotenv()

# Global ML models
career_classifier = None
salary_predictor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global career_classifier, salary_predictor
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize ML models
    career_classifier = CareerClassifier()
    salary_predictor = SalaryPredictor()
    
    print("🚀 CareerAI Backend Started Successfully!")
    print("📊 ML Models Loaded")
    print("🗄️ Database Connected")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down CareerAI Backend...")

app = FastAPI(
    title="CareerAI API",
    description="Intelligent Career Path Prediction & Skill Gap Analyzer",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://careerai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(career_prediction.router, prefix="/api", tags=["Career Prediction"])
app.include_router(github_analysis.router, prefix="/api", tags=["GitHub Analysis"])
app.include_router(skill_gap.router, prefix="/api", tags=["Skill Gap"])
app.include_router(roadmap.router, prefix="/api", tags=["Roadmap Generation"])

@app.get("/")
async def root():
    return {
        "message": "CareerAI API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "auth": "/api/auth",
            "career_prediction": "/api/predict-career",
            "github_analysis": "/api/analyze-github",
            "skill_gap": "/api/skill-gap",
            "roadmap": "/api/generate-roadmap"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": {
            "career_classifier": career_classifier is not None,
            "salary_predictor": salary_predictor is not None
        },
        "database": "connected"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
