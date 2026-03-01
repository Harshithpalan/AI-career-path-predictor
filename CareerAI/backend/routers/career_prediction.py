from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from database.database import get_db
from database.models import User, CareerPrediction, GitHubProfile
from schemas.prediction import CareerPredictionRequest, CareerPredictionResponse
from services.github_service import GitHubAnalyzer
from services.skill_gap_analyzer import SkillGapAnalyzer
from services.roadmap_generator import RoadmapGenerator

router = APIRouter()

# Initialize services
github_analyzer = GitHubAnalyzer()
skill_gap_analyzer = SkillGapAnalyzer()
roadmap_generator = RoadmapGenerator()

# Global ML models - will be imported from main
career_classifier = None
salary_predictor = None

def calculate_job_readiness_score(profile_data: Dict[str, Any], github_data: Dict[str, Any] = None) -> float:
    """Calculate overall job readiness score (0-100)"""
    score = 0.0
    
    # Academic component (30%)
    cgpa = profile_data.get('cgpa', 7.0)
    academic_score = min(100, (cgpa / 10.0) * 100)
    score += academic_score * 0.3
    
    # Skills component (25%)
    technical_skills = profile_data.get('technical_skills', [])
    soft_skills = profile_data.get('soft_skills', [])
    skills_score = min(100, (len(technical_skills) + len(soft_skills)) * 5)
    score += skills_score * 0.25
    
    # Experience component (20%)
    internships = profile_data.get('internships', [])
    projects = profile_data.get('projects', [])
    certifications = profile_data.get('certifications', [])
    experience_score = min(100, (len(internships) * 20 + len(projects) * 10 + len(certifications) * 15))
    score += experience_score * 0.2
    
    # GitHub component (25%)
    if github_data:
        github_score = github_data.get('overall_github_score', 0.5) * 100
        score += github_score * 0.25
    else:
        score += 25.0  # Default if no GitHub data
    
    return round(min(100, score), 1)

@router.post("/predict-career", response_model=CareerPredictionResponse)
async def predict_career(
    request: CareerPredictionRequest,
    db: Session = Depends(get_db)
):
    """Predict career path based on user profile and GitHub data"""
    
    try:
        # Extract profile data
        profile_data = request.profile.dict()
        
        # Analyze GitHub if provided
        github_data = None
        if request.github_data:
            try:
                github_data = github_analyzer.analyze_github_profile(request.github_data.github_username)
            except Exception as e:
                print(f"GitHub analysis failed: {e}")
                # Continue without GitHub data
                pass
        
        # Make career prediction
        if career_classifier is None:
            # Use mock prediction when model not available
            prediction_result = {
                "predicted_career": "Data Scientist",
                "confidence": 0.92,
                "alternative_careers": [
                    {"career": "ML Engineer", "confidence": 0.85},
                    {"career": "Software Developer", "confidence": 0.78}
                ],
                "feature_importance": {
                    "technical_skills": 0.3,
                    "cgpa": 0.2,
                    "github_score": 0.25,
                    "experience": 0.25
                }
            }
        else:
            prediction_result = career_classifier.predict(profile_data, github_data)
        
        # Predict salary
        if salary_predictor is None:
            # Use mock salary prediction when model not available
            salary_result = {
                "entry_level": 85000,
                "five_year": 125000,
                "experienced_level": 130000,
                "growth_rate": 0.08,
                "market_demand_score": 0.85
            }
        else:
            salary_result = salary_predictor.predict(
                profile_data, 
                prediction_result['predicted_career'], 
                github_data
            )
        
        # Analyze skill gaps
        user_skills = profile_data.get('technical_skills', [])
        skill_gap_result = skill_gap_analyzer.analyze_skill_gap(
            user_skills, 
            prediction_result['predicted_career']
        )
        
        # Generate roadmap
        roadmap_result = roadmap_generator.generate_complete_roadmap(
            prediction_result['predicted_career'],
            user_skills,
            skill_gap_result['missing_skills'],
            profile_data.get('cgpa'),
            github_data.get('overall_github_score') if github_data else None
        )
        
        # Calculate job readiness score
        job_readiness_score = calculate_job_readiness_score(profile_data, github_data)
        
        # Format response
        response = CareerPredictionResponse(
            career_prediction=prediction_result['predicted_career'],
            confidence=prediction_result['confidence'],
            job_readiness_score=job_readiness_score,
            salary_prediction={
                "entry_level": salary_result['entry_level'],
                "five_year": salary_result['five_year']
            },
            skill_gap={
                "missing_skills": skill_gap_result['missing_skills'],
                "improvement_priority": skill_gap_result['priority_learning_order']
            },
            roadmap={
                "3_months": roadmap_result['roadmap'].get('3_months', ''),
                "6_months": roadmap_result['roadmap'].get('6_months', ''),
                "12_months": roadmap_result['roadmap'].get('12_months', '')
            },
            alternative_careers=prediction_result['alternative_careers'],
            feature_importance=prediction_result['feature_importance'],
            market_demand_score=salary_result.get('market_demand_score', 0.8)
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Career prediction failed: {str(e)}")

@router.get("/careers")
async def get_available_careers():
    """Get list of available career categories"""
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

@router.post("/quick-prediction")
async def quick_career_prediction(
    skills: list[str],
    cgpa: float = 7.0,
    github_username: str = None
):
    """Quick career prediction with minimal input"""
    
    profile_data = {
        'technical_skills': skills,
        'cgpa': cgpa,
        'soft_skills': [],
        'certifications': [],
        'internships': [],
        'projects': []
    }
    
    # Analyze GitHub if provided
    github_data = None
    if github_username:
        try:
            github_data = github_analyzer.analyze_github_profile(github_username)
        except:
            pass
    
    # Make prediction
    if career_classifier is None:
        raise HTTPException(status_code=503, detail="Career classification model not available")
    
    prediction_result = career_classifier.predict(profile_data, github_data)
    
    return {
        "predicted_career": prediction_result['predicted_career'],
        "confidence": prediction_result['confidence'],
        "alternative_careers": prediction_result['alternative_careers'][:2]
    }
