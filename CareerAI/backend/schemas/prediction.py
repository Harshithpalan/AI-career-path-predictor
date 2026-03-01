from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class UserProfileInput(BaseModel):
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    degree: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    certifications: List[str] = []
    internships: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    interests: List[str] = []
    preferred_industries: List[str] = []

class GitHubAnalysisInput(BaseModel):
    github_username: str = Field(..., min_length=1, max_length=39)
    include_private_repos: bool = False

class CareerPredictionRequest(BaseModel):
    profile: UserProfileInput
    github_data: Optional[GitHubAnalysisInput] = None

class CareerPredictionResponse(BaseModel):
    career_prediction: str
    confidence: float
    job_readiness_score: float
    salary_prediction: Dict[str, float]
    skill_gap: Dict[str, List[str]]
    roadmap: Dict[str, str]
    alternative_careers: List[Dict[str, Any]]
    feature_importance: Dict[str, float]
    market_demand_score: float

class GitHubProfileResponse(BaseModel):
    github_username: str
    total_repos: int
    public_repos: int
    followers: int
    following: int
    total_commits: int
    primary_languages: List[str]
    language_percentages: Dict[str, float]
    commit_frequency: float
    contribution_consistency: float
    project_complexity_score: float
    ml_orientation: float
    web_orientation: float
    systems_orientation: float
    innovation_score: float
    consistency_score: float
    depth_score: float
    overall_github_score: float

class SkillGapRequest(BaseModel):
    user_skills: List[str]
    target_career: str

class SkillGapResponse(BaseModel):
    missing_skills: List[str]
    weak_skills: List[str]
    improvement_priority: List[str]
    current_skill_score: float
    target_skill_score: float
    gap_percentage: float
    recommended_courses: List[Dict[str, str]]
    recommended_certifications: List[str]
    recommended_projects: List[str]

class RoadmapRequest(BaseModel):
    career: str
    current_skills: List[str]
    missing_skills: List[str]
    cgpa: Optional[float] = None
    github_score: Optional[float] = None

class RoadmapResponse(BaseModel):
    three_month_plan: str
    six_month_plan: str
    twelve_month_plan: str
    project_ideas: List[Dict[str, str]]
    interview_preparation: Dict[str, List[str]]
    resume_improvements: List[str]
    recommended_resources: List[Dict[str, str]]
    milestone_checkpoints: List[Dict[str, str]]

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    github_username: Optional[str]
    linkedin_url: Optional[str]
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
