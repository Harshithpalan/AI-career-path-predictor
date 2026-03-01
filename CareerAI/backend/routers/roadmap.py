from fastapi import APIRouter, HTTPException
from schemas.prediction import RoadmapRequest, RoadmapResponse
from services.roadmap_generator import RoadmapGenerator

router = APIRouter()
roadmap_generator = RoadmapGenerator()

@router.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """Generate personalized career roadmap"""
    
    try:
        result = roadmap_generator.generate_complete_roadmap(
            request.career,
            request.current_skills,
            request.missing_skills,
            request.cgpa,
            request.github_score
        )
        
        # Format response according to schema
        roadmap_plans = result['roadmap']
        
        return RoadmapResponse(
            three_month_plan=roadmap_plans.get('3_months', ''),
            six_month_plan=roadmap_plans.get('6_months', ''),
            twelve_month_plan=roadmap_plans.get('12_months', ''),
            project_ideas=result['project_ideas'],
            interview_preparation=result['interview_preparation'],
            resume_improvements=result['resume_improvements'],
            recommended_resources=result['recommended_resources'],
            milestone_checkpoints=result['milestone_checkpoints']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roadmap generation failed: {str(e)}")

@router.get("/roadmap-template/{career}")
async def get_roadmap_template(career: str):
    """Get roadmap template for a specific career"""
    
    try:
        template = roadmap_generator.generate_template_roadmap(career, [], [])
        
        return {
            "career": career,
            "roadmap": template
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap template: {str(e)}")

@router.get("/project-ideas/{career}")
async def get_project_ideas(career: str, skills: list[str] = []):
    """Get project ideas for a specific career"""
    
    try:
        projects = roadmap_generator.get_project_ideas(career, skills)
        
        return {
            "career": career,
            "project_ideas": projects
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get project ideas: {str(e)}")

@router.get("/interview-prep/{career}")
async def get_interview_preparation(career: str):
    """Get interview preparation for a specific career"""
    
    try:
        prep = roadmap_generator.get_interview_preparation(career)
        
        return {
            "career": career,
            "interview_preparation": prep
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get interview preparation: {str(e)}")
