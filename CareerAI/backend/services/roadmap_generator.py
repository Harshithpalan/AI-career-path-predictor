from typing import Dict, List, Any
import openai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class RoadmapGenerator:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Career-specific project templates
        self.project_templates = {
            'Data Scientist': [
                {
                    'title': 'Customer Churn Prediction System',
                    'description': 'Build an ML model to predict customer churn with data preprocessing, feature engineering, and deployment',
                    'skills': ['python', 'machine_learning', 'data_analysis', 'visualization'],
                    'duration': '6-8 weeks',
                    'difficulty': 'Intermediate'
                },
                {
                    'title': 'Real-time Sentiment Analysis Dashboard',
                    'description': 'Create a dashboard that analyzes social media sentiment in real-time using NLP techniques',
                    'skills': ['python', 'nlp', 'api_integration', 'dashboarding'],
                    'duration': '4-6 weeks',
                    'difficulty': 'Intermediate'
                },
                {
                    'title': 'Financial Risk Assessment Model',
                    'description': 'Develop a comprehensive risk assessment system for loan applications using ensemble methods',
                    'skills': ['python', 'statistics', 'ensemble_methods', 'feature_engineering'],
                    'duration': '8-10 weeks',
                    'difficulty': 'Advanced'
                }
            ],
            'ML Engineer': [
                {
                    'title': 'ML Model Deployment Pipeline',
                    'description': 'Build an end-to-end MLOps pipeline with model training, validation, and deployment',
                    'skills': ['python', 'docker', 'kubernetes', 'ci_cd', 'ml_ops'],
                    'duration': '8-10 weeks',
                    'difficulty': 'Advanced'
                },
                {
                    'title': 'Computer Vision API Service',
                    'description': 'Create a RESTful API for image classification with model monitoring and retraining',
                    'skills': ['python', 'deep_learning', 'fastapi', 'docker', 'monitoring'],
                    'duration': '6-8 weeks',
                    'difficulty': 'Intermediate'
                },
                {
                    'title': 'Real-time Fraud Detection System',
                    'description': 'Build a streaming ML system for real-time fraud detection with auto-scaling',
                    'skills': ['python', 'streaming', 'machine_learning', 'kafka', 'spark'],
                    'duration': '10-12 weeks',
                    'difficulty': 'Advanced'
                }
            ],
            'Software Developer': [
                {
                    'title': 'Microservices E-commerce Platform',
                    'description': 'Design and implement a scalable e-commerce platform using microservices architecture',
                    'skills': ['backend', 'databases', 'api_design', 'system_design'],
                    'duration': '10-12 weeks',
                    'difficulty': 'Advanced'
                },
                {
                    'title': 'Real-time Collaboration Tool',
                    'description': 'Build a real-time collaborative application with WebSockets and conflict resolution',
                    'skills': ['websockets', 'real_time', 'algorithms', 'concurrency'],
                    'duration': '6-8 weeks',
                    'difficulty': 'Intermediate'
                },
                {
                    'title': 'Performance Monitoring System',
                    'description': 'Create a comprehensive application performance monitoring and alerting system',
                    'skills': ['monitoring', 'algorithms', 'data_structures', 'optimization'],
                    'duration': '8-10 weeks',
                    'difficulty': 'Intermediate'
                }
            ],
            'Full Stack Developer': [
                {
                    'title': 'Social Media Platform',
                    'description': 'Build a full-featured social media platform with real-time updates and mobile responsiveness',
                    'skills': ['react', 'nodejs', 'databases', 'authentication', 'real_time'],
                    'duration': '12-14 weeks',
                    'difficulty': 'Advanced'
                },
                {
                    'title': 'Project Management SaaS',
                    'description': 'Create a comprehensive project management tool with team collaboration features',
                    'skills': ['frontend', 'backend', 'api_design', 'authentication', 'database'],
                    'duration': '10-12 weeks',
                    'difficulty': 'Intermediate'
                },
                {
                    'title': 'E-commerce Marketplace',
                    'description': 'Develop a multi-vendor e-commerce platform with payment integration and inventory management',
                    'skills': ['full_stack', 'payment_integration', 'database', 'api'],
                    'duration': '12-14 weeks',
                    'difficulty': 'Advanced'
                }
            ]
        }
        
        # Interview preparation templates
        self.interview_templates = {
            'technical': {
                'Data Scientist': [
                    'Explain the bias-variance tradeoff',
                    'How would you handle missing data?',
                    'Describe cross-validation techniques',
                    'Explain regularization methods',
                    'How do you evaluate model performance?'
                ],
                'ML Engineer': [
                    'Explain model deployment strategies',
                    'How do you handle model drift?',
                    'Describe MLOps best practices',
                    'Explain containerization benefits',
                    'How do you monitor ML models?'
                ],
                'Software Developer': [
                    'Explain SOLID principles',
                    'Describe design patterns',
                    'How do you handle concurrency?',
                    'Explain database indexing',
                    'Describe system design approach'
                ]
            },
            'behavioral': [
                'Tell me about a challenging project',
                'How do you handle tight deadlines?',
                'Describe a time you failed',
                'How do you stay updated with technology?',
                'Explain your problem-solving approach'
            ]
        }
    
    def generate_llm_roadmap(self, career: str, current_skills: List[str], missing_skills: List[str], 
                           cgpa: float, github_score: float) -> Dict[str, str]:
        """Generate personalized roadmap using LLM"""
        
        prompt = f"""
        You are a senior career strategist and technical mentor. Create a personalized career roadmap for a student.

        Student Profile:
        - Target Career: {career}
        - Current Skills: {', '.join(current_skills)}
        - Missing Skills: {', '.join(missing_skills[:5])}
        - CGPA: {cgpa}
        - GitHub Strength: {github_score}

        Generate a comprehensive roadmap with:
        1. 3-month action plan (focus on fundamentals)
        2. 6-month roadmap (intermediate skills)
        3. 12-month mastery strategy (advanced topics)

        Make it practical, realistic, and specific. Include:
        - Specific learning resources
        - Project suggestions
        - Skill milestones
        - Timeline with weekly goals

        Format as JSON with keys: "3_months", "6_months", "12_months"
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career advisor and technical mentor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            import json
            roadmap = json.loads(response.choices[0].message.content)
            return roadmap
            
        except Exception as e:
            # Fallback to template-based roadmap
            return self.generate_template_roadmap(career, current_skills, missing_skills)
    
    def generate_template_roadmap(self, career: str, current_skills: List[str], missing_skills: List[str]) -> Dict[str, str]:
        """Generate roadmap from templates (fallback method)"""
        
        roadmap_templates = {
            '3_months': self._generate_3_month_plan(career, current_skills, missing_skills),
            '6_months': self._generate_6_month_plan(career, current_skills, missing_skills),
            '12_months': self._generate_12_month_plan(career, current_skills, missing_skills)
        }
        
        return roadmap_templates
    
    def _generate_3_month_plan(self, career: str, current_skills: List[str], missing_skills: List[str]) -> str:
        """Generate 3-month focused plan"""
        
        if 'Data Scientist' in career:
            return """
            **Months 1-3: Foundation Building**
            
            **Month 1: Core Skills**
            - Week 1-2: Master Python for data science (NumPy, Pandas)
            - Week 3-4: Statistics fundamentals and probability theory
            
            **Month 2: Machine Learning Basics**
            - Week 5-6: Linear regression, logistic regression, decision trees
            - Week 7-8: Model evaluation and cross-validation
            
            **Month 3: Practical Application**
            - Week 9-10: Complete first ML project (e.g., house price prediction)
            - Week 11-12: Data visualization with Matplotlib/Seaborn
            
            **Key Milestones:**
            - Complete 2 beginner ML projects
            - Achieve 80%+ in online statistics course
            - Build portfolio with clean, documented code
            """
        
        elif 'ML Engineer' in career:
            return """
            **Months 1-3: Engineering Foundation**
            
            **Month 1: Software Engineering**
            - Week 1-2: Advanced Python and OOP concepts
            - Week 3-4: System design fundamentals
            
            **Month 2: ML Engineering Basics**
            - Week 5-6: ML model deployment concepts
            - Week 7-8: Docker and containerization basics
            
            **Month 3: Infrastructure**
            - Week 9-10: Cloud platforms (AWS/Azure basics)
            - Week 11-12: CI/CD pipeline fundamentals
            
            **Key Milestones:**
            - Containerize a simple ML model
            - Deploy model to cloud platform
            - Build automated testing pipeline
            """
        
        else:  # Default for other careers
            return f"""
            **Months 1-3: Foundation Building for {career}**
            
            **Month 1: Core Fundamentals**
            - Week 1-2: Programming fundamentals and best practices
            - Week 3-4: Domain-specific concepts and terminology
            
            **Month 2: Skill Development**
            - Week 5-6: Essential tools and technologies
            - Week 7-8: Hands-on practice with small projects
            
            **Month 3: Practical Application**
            - Week 9-10: Build first complete project
            - Week 11-12: Portfolio development and documentation
            
            **Key Milestones:**
            - Complete foundational online course
            - Build first portfolio project
            - Establish consistent coding practice
            """
    
    def _generate_6_month_plan(self, career: str, current_skills: List[str], missing_skills: List[str]) -> str:
        """Generate 6-month intermediate plan"""
        
        return f"""
        **Months 4-6: Intermediate Development for {career}**
        
        **Month 4: Advanced Concepts**
        - Deep dive into core technologies
        - Advanced algorithms and data structures
        - Industry best practices and patterns
        
        **Month 5: Specialization**
        - Focus on career-specific technologies
        - Build complex, multi-component projects
        - Learn debugging and optimization techniques
        
        **Month 6: Portfolio Enhancement**
        - Complete 2-3 significant projects
        - Contribute to open source if applicable
        - Start networking and community engagement
        
        **Key Milestones:**
        - Master 3-5 core technologies
        - Build impressive portfolio projects
        - Establish professional online presence
        """
    
    def _generate_12_month_plan(self, career: str, current_skills: List[str], missing_skills: List[str]) -> str:
        """Generate 12-month mastery strategy"""
        
        return f"""
        **Months 7-12: Advanced Mastery for {career}**
        
        **Months 7-9: Advanced Topics**
        - Cutting-edge technologies and frameworks
        - System architecture and scalability
        - Performance optimization and security
        
        **Months 10-11: Professional Development**
        - Leadership and communication skills
        - Project management and teamwork
        - Industry certifications and advanced training
        
        **Month 12: Career Launch**
        - Resume optimization and interview preparation
        - Job search strategy and networking
        - Final portfolio polish and personal branding
        
        **Key Milestones:**
        - Achieve expert-level in core technologies
        - Complete capstone project demonstrating mastery
        - Obtain relevant certifications
        - Secure internship or entry-level position
        """
    
    def get_project_ideas(self, career: str, current_skills: List[str]) -> List[Dict[str, str]]:
        """Get project ideas based on career and skills"""
        
        if career in self.project_templates:
            projects = self.project_templates[career]
            
            # Score projects based on current skills
            scored_projects = []
            for project in projects:
                score = 0
                for skill in current_skills:
                    if skill.lower() in str(project['skills']).lower():
                        score += 1
                
                scored_projects.append({
                    **project,
                    'relevance_score': score
                })
            
            # Sort by relevance and return top 3
            scored_projects.sort(key=lambda x: x['relevance_score'], reverse=True)
            return scored_projects[:3]
        
        # Default projects for other careers
        return [
            {
                'title': 'Career-Specific Portfolio Project',
                'description': f'Build a comprehensive project demonstrating {career} skills',
                'skills': current_skills[:3] if current_skills else ['problem_solving'],
                'duration': '8-10 weeks',
                'difficulty': 'Intermediate'
            }
        ]
    
    def get_interview_preparation(self, career: str) -> Dict[str, List[str]]:
        """Get interview preparation strategy"""
        
        technical_questions = self.interview_templates['technical'].get(career, [])
        behavioral_questions = self.interview_templates['behavioral']
        
        return {
            'technical_questions': technical_questions[:5],
            'behavioral_questions': behavioral_questions[:5],
            'preparation_tips': [
                'Practice coding challenges daily',
                'Prepare STAR method for behavioral questions',
                'Research company and role thoroughly',
                'Prepare thoughtful questions for interviewer',
                'Practice mock interviews with peers'
            ]
        }
    
    def get_resume_improvements(self, career: str, current_skills: List[str], missing_skills: List[str]) -> List[str]:
        """Get resume improvement suggestions"""
        
        suggestions = [
            f"Quantify achievements with specific metrics and results",
            f"Highlight {career}-specific projects and experiences",
            f"Include relevant keywords from job descriptions",
            f"Showcase technical skills with practical examples",
            f"Add GitHub portfolio link with active contributions",
            f"Include certifications and online courses",
            f"Emphasize problem-solving and impact",
            f"Use action verbs and clear, concise language"
        ]
        
        if missing_skills:
            suggestions.append(f"Plan to acquire missing skills: {', '.join(missing_skills[:3])}")
        
        if not current_skills:
            suggestions.append("Focus on building foundational skills first")
        
        return suggestions
    
    def generate_complete_roadmap(self, career: str, current_skills: List[str], missing_skills: List[str],
                                cgpa: float = None, github_score: float = None) -> Dict[str, Any]:
        """Generate complete personalized roadmap"""
        
        # Try LLM generation first
        try:
            roadmap_plans = self.generate_llm_roadmap(career, current_skills, missing_skills, cgpa, github_score)
        except:
            roadmap_plans = self.generate_template_roadmap(career, current_skills, missing_skills)
        
        # Get additional components
        project_ideas = self.get_project_ideas(career, current_skills)
        interview_prep = self.get_interview_preparation(career)
        resume_improvements = self.get_resume_improvements(career, current_skills, missing_skills)
        
        # Generate milestone checkpoints
        milestones = self._generate_milestones(career, current_skills, missing_skills)
        
        # Recommended resources
        resources = self._generate_resources(career, missing_skills)
        
        return {
            'roadmap': roadmap_plans,
            'project_ideas': project_ideas,
            'interview_preparation': interview_prep,
            'resume_improvements': resume_improvements,
            'milestone_checkpoints': milestones,
            'recommended_resources': resources
        }
    
    def _generate_milestones(self, career: str, current_skills: List[str], missing_skills: List[str]) -> List[Dict[str, str]]:
        """Generate milestone checkpoints"""
        
        return [
            {
                'timeline': '3 months',
                'milestone': 'Foundation Complete',
                'criteria': 'Master core concepts, complete 2 basic projects'
            },
            {
                'timeline': '6 months',
                'milestone': 'Intermediate Proficiency',
                'criteria': 'Build complex project, contribute to open source'
            },
            {
                'timeline': '9 months',
                'milestone': 'Advanced Skills',
                'criteria': 'Complete capstone project, obtain certification'
            },
            {
                'timeline': '12 months',
                'milestone': 'Career Ready',
                'criteria': 'Strong portfolio, interview ready, job applications'
            }
        ]
    
    def _generate_resources(self, career: str, missing_skills: List[str]) -> List[Dict[str, str]]:
        """Generate recommended learning resources"""
        
        resources = []
        
        # Career-specific resources
        career_resources = {
            'Data Scientist': [
                {'type': 'Course', 'name': 'Machine Learning by Andrew Ng', 'provider': 'Coursera'},
                {'type': 'Book', 'name': 'Introduction to Statistical Learning', 'provider': 'Springer'},
                {'type': 'Platform', 'name': 'Kaggle Competitions', 'provider': 'Kaggle'}
            ],
            'ML Engineer': [
                {'type': 'Course', 'name': 'MLOps Specialization', 'provider': 'Coursera'},
                {'type': 'Book', 'name': 'Designing Machine Learning Systems', 'provider': "O'Reilly"},
                {'type': 'Platform', 'name': 'Docker Hub', 'provider': 'Docker'}
            ],
            'Software Developer': [
                {'type': 'Course', 'name': 'System Design', 'provider': 'Grokking the System Design'},
                {'type': 'Book', 'name': 'Clean Code', 'provider': 'Prentice Hall'},
                {'type': 'Platform', 'name': 'LeetCode', 'provider': 'LeetCode'}
            ]
        }
        
        if career in career_resources:
            resources.extend(career_resources[career])
        
        # Skill-specific resources
        for skill in missing_skills[:3]:
            skill_resources = {
                'python': [{'type': 'Course', 'name': 'Python for Everybody', 'provider': 'Coursera'}],
                'aws': [{'type': 'Course', 'name': 'AWS Cloud Practitioner', 'provider': 'AWS Training'}],
                'docker': [{'type': 'Course', 'name': 'Docker Mastery', 'provider': 'Udemy'}],
                'react': [{'type': 'Course', 'name': 'Modern React', 'provider': 'Udemy'}]
            }
            
            if skill.lower() in skill_resources:
                resources.extend(skill_resources[skill.lower()])
        
        return resources[:8]  # Return top 8 resources
