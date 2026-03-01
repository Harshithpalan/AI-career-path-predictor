from fastapi import APIRouter, HTTPException
from schemas.prediction import SkillGapRequest, SkillGapResponse
from services.skill_gap_analyzer import SkillGapAnalyzer

router = APIRouter()
skill_gap_analyzer = SkillGapAnalyzer()

@router.post("/skill-gap", response_model=SkillGapResponse)
async def analyze_skill_gap(request: SkillGapRequest):
    """Analyze skill gaps for target career"""
    
    try:
        result = skill_gap_analyzer.analyze_skill_gap(
            request.user_skills,
            request.target_career
        )
        
        return SkillGapResponse(
            missing_skills=result['missing_skills'],
            weak_skills=result['weak_skills'],
            improvement_priority=result['priority_learning_order'],
            current_skill_score=result['current_skill_score'],
            target_skill_score=result['target_skill_score'],
            gap_percentage=result['gap_percentage'],
            recommended_courses=result['recommended_courses'],
            recommended_certifications=result['recommended_certifications'],
            recommended_projects=result['recommended_projects']
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill gap analysis failed: {str(e)}")

@router.get("/skill-requirements/{career}")
async def get_career_skill_requirements(career: str):
    """Get skill requirements for a specific career"""
    
    try:
        if career not in skill_gap_analyzer.career_skill_requirements:
            raise HTTPException(status_code=404, detail=f"Career '{career}' not found")
        
        requirements = skill_gap_analyzer.career_skill_requirements[career]
        
        return {
            "career": career,
            "essential_skills": requirements['essential'],
            "important_skills": requirements['important'],
            "bonus_skills": requirements['bonus'],
            "total_skills": len(requirements['essential']) + len(requirements['important']) + len(requirements['bonus'])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch skill requirements: {str(e)}")

@router.post("/skill-similarity")
async def calculate_skill_similarity(skills1: list[str], skills2: list[str]):
    """Calculate similarity between two skill sets"""
    
    try:
        similarity = skill_gap_analyzer.calculate_skill_similarity(skills1, skills2)
        
        return {
            "skills1": skills1,
            "skills2": skills2,
            "similarity_score": round(similarity, 3),
            "similarity_percentage": round(similarity * 100, 1)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similarity calculation failed: {str(e)}")
