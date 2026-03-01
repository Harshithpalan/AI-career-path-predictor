from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    github_username = Column(String)
    linkedin_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    profiles = relationship("UserProfile", back_populates="user")
    predictions = relationship("CareerPrediction", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Academic Information
    cgpa = Column(Float)
    degree = Column(String)
    university = Column(String)
    graduation_year = Column(Integer)
    
    # Skills
    technical_skills = Column(JSON)  # List of technical skills
    soft_skills = Column(JSON)       # List of soft skills
    certifications = Column(JSON)    # List of certifications
    
    # Experience
    internships = Column(JSON)       # List of internship experiences
    projects = Column(JSON)          # List of personal projects
    
    # Interests
    interests = Column(JSON)         # Career interests
    preferred_industries = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profiles")

class GitHubProfile(Base):
    __tablename__ = "github_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    github_username = Column(String, nullable=False)
    
    # GitHub Stats
    total_repos = Column(Integer)
    public_repos = Column(Integer)
    followers = Column(Integer)
    following = Column(Integer)
    total_commits = Column(Integer)
    
    # Language Analysis
    primary_languages = Column(JSON)
    language_percentages = Column(JSON)
    
    # Activity Metrics
    commit_frequency = Column(Float)
    contribution_consistency = Column(Float)
    project_complexity_score = Column(Float)
    
    # Specialization Scores
    ml_orientation = Column(Float)
    web_orientation = Column(Float)
    systems_orientation = Column(Float)
    innovation_score = Column(Float)
    
    # Raw Data
    raw_data = Column(JSON)  # Store complete GitHub API response
    
    last_analyzed = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CareerPrediction(Base):
    __tablename__ = "career_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Prediction Results
    predicted_career = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    alternative_careers = Column(JSON)  # Top 3 alternatives with scores
    
    # Salary Predictions
    entry_salary = Column(Float)
    five_year_salary = Column(Float)
    market_demand_score = Column(Float)
    
    # Job Readiness
    job_readiness_score = Column(Float)
    skill_gap_score = Column(Float)
    
    # Analysis Details
    feature_importance = Column(JSON)
    model_version = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="predictions")

class SkillGapAnalysis(Base):
    __tablename__ = "skill_gap_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_career = Column(String, nullable=False)
    
    # Gap Analysis
    missing_skills = Column(JSON)
    weak_skills = Column(JSON)
    priority_learning_order = Column(JSON)
    
    # Skill Scores
    current_skill_score = Column(Float)
    target_skill_score = Column(Float)
    gap_percentage = Column(Float)
    
    # Recommendations
    recommended_courses = Column(JSON)
    recommended_certifications = Column(JSON)
    recommended_projects = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PersonalizedRoadmap(Base):
    __tablename__ = "personalized_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_career = Column(String, nullable=False)
    
    # Roadmap Content
    three_month_plan = Column(JSON)
    six_month_plan = Column(JSON)
    twelve_month_plan = Column(JSON)
    
    # Specific Recommendations
    project_ideas = Column(JSON)
    interview_prep_strategy = Column(JSON)
    resume_improvements = Column(JSON)
    
    # Learning Resources
    recommended_resources = Column(JSON)
    milestone_checkpoints = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    career_title = Column(String, nullable=False)
    
    # Market Trends
    average_entry_salary = Column(Float)
    average_experienced_salary = Column(Float)
    job_growth_rate = Column(Float)
    market_demand_score = Column(Float)
    
    # Required Skills
    required_skills = Column(JSON)
    skill_importance_weights = Column(JSON)
    
    # Regional Data
    regional_salary_data = Column(JSON)
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
