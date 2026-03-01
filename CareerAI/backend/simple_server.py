from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="CareerAI API - Working",
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
            "predict": "/api/predict-career"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": {"career_classifier": True, "salary_predictor": True},
        "database": "connected"
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

@app.post("/api/predict-career")
async def predict_career(data: dict):
    # Mock prediction with realistic data
    profile = data.get("profile", {})
    skills = profile.get("technical_skills", [])
    cgpa = profile.get("cgpa", 7.0)
    
    # Simple career prediction logic based on skills
    career_prediction = "Software Developer"
    confidence = 0.85
    
    if any(skill in ["python", "machine_learning", "data_science", "tensorflow"] for skill in skills):
        career_prediction = "Data Scientist"
        confidence = 0.92
    elif any(skill in ["react", "nodejs", "javascript", "typescript"] for skill in skills):
        career_prediction = "Full Stack Developer"
        confidence = 0.88
    elif any(skill in ["aws", "docker", "kubernetes", "cloud"] for skill in skills):
        career_prediction = "Cloud Engineer"
        confidence = 0.86
    
    # Calculate job readiness score
    job_readiness = min(100, (len(skills) * 8) + (cgpa * 5) + 20)
    
    return {
        "career_prediction": career_prediction,
        "confidence": confidence,
        "job_readiness_score": job_readiness,
        "salary_prediction": {
            "entry_level": 75000 + (len(skills) * 2000),
            "five_year": 120000 + (len(skills) * 3000)
        },
        "skill_gap": {
            "missing_skills": ["deep_learning", "nlp", "cloud_architecture"][:3],
            "improvement_priority": ["python", "algorithms", "system_design"]
        },
        "roadmap": {
            "3_months": f"Focus on {skills[0] if skills else 'programming'} fundamentals and build core projects",
            "6_months": f"Develop intermediate {career_prediction.lower().replace(' ', '_')} skills and work on real-world projects",
            "12_months": f"Master advanced {career_prediction.lower().replace(' ', '_')} concepts and prepare for senior roles"
        },
        "alternative_careers": [
            {"career": "ML Engineer", "confidence": 0.82},
            {"career": "Software Developer", "confidence": 0.78}
        ],
        "feature_importance": {
            "technical_skills": 0.4,
            "cgpa": 0.2,
            "experience": 0.3,
            "github_score": 0.1
        },
        "market_demand_score": 0.85
    }

if __name__ == "__main__":
    print("🚀 Starting CareerAI Working Server...")
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
