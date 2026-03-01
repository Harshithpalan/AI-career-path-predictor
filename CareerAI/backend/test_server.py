from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="CareerAI API - Test",
    description="Intelligent Career Path Prediction & Skill Gap Analyzer",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "https://careerai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "CareerAI API is running!",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "careers": "/careers",
            "predict": "/predict-career"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "CareerAI backend is running successfully"
    }

@app.get("/careers")
async def get_careers():
    return {
        "careers": [
            "Data Scientist",
            "ML Engineer", 
            "Software Developer",
            "Full Stack Developer",
            "Cybersecurity Analyst",
            "Cloud Engineer",
            "DevOps Engineer",
            "Researcher",
            "Product Manager",
            "UI/UX Engineer"
        ]
    }

@app.post("/predict-career")
async def predict_career_test(data: dict):
    # Mock prediction for testing
    return {
        "career_prediction": "Data Scientist",
        "confidence": 0.92,
        "job_readiness_score": 78.5,
        "salary_prediction": {
            "entry_level": 85000,
            "five_year": 125000
        },
        "skill_gap": {
            "missing_skills": ["deep_learning", "nlp"],
            "improvement_priority": ["python", "statistics", "machine_learning"]
        },
        "roadmap": {
            "3_months": "Focus on Python and Statistics fundamentals",
            "6_months": "Learn Machine Learning algorithms",
            "12_months": "Master Deep Learning and NLP"
        }
    }

if __name__ == "__main__":
    print("🚀 Starting CareerAI Test Server...")
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
