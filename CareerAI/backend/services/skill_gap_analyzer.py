from typing import Dict, List, Any, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
import os
from dotenv import load_dotenv

load_dotenv()

class SkillGapAnalyzer:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        # Career skill requirements (comprehensive skill database)
        self.career_skill_requirements = {
            'Data Scientist': {
                'essential': [
                    'python', 'statistics', 'machine_learning', 'data_analysis', 
                    'sql', 'pandas', 'numpy', 'data_visualization', 'probability'
                ],
                'important': [
                    'tensorflow', 'pytorch', 'scikit-learn', 'r', 'tableau', 
                    'power_bi', 'deep_learning', 'nlp', 'time_series'
                ],
                'bonus': [
                    'spark', 'hadoop', 'aws', 'azure', 'gcp', 'mlops', 
                    'kubernetes', 'docker', 'git', 'communication'
                ]
            },
            'ML Engineer': {
                'essential': [
                    'python', 'machine_learning', 'deep_learning', 'tensorflow', 
                    'pytorch', 'algorithms', 'data_structures', 'software_engineering'
                ],
                'important': [
                    'mlops', 'docker', 'kubernetes', 'ci_cd', 'aws', 'azure', 
                    'scikit-learn', 'nlp', 'computer_vision', 'git'
                ],
                'bonus': [
                    'microservices', 'api_design', 'testing', 'monitoring', 
                    'spark', 'kafka', 'airflow', 'fastapi', 'system_design'
                ]
            },
            'Software Developer': {
                'essential': [
                    'programming', 'algorithms', 'data_structures', 'oop', 
                    'git', 'testing', 'debugging', 'problem_solving'
                ],
                'important': [
                    'python', 'java', 'javascript', 'c++', 'sql', 'api_design', 
                    'system_design', 'design_patterns', 'version_control'
                ],
                'bonus': [
                    'docker', 'aws', 'kubernetes', 'ci_cd', 'agile', 
                    'unit_testing', 'code_review', 'performance_optimization'
                ]
            },
            'Full Stack Developer': {
                'essential': [
                    'javascript', 'html', 'css', 'react', 'nodejs', 'api_design', 
                    'databases', 'git', 'frontend', 'backend'
                ],
                'important': [
                    'typescript', 'vue', 'angular', 'mongodb', 'postgresql', 
                    'express', 'rest_api', 'authentication', 'deployment'
                ],
                'bonus': [
                    'nextjs', 'graphql', 'redis', 'docker', 'aws', 'testing', 
                    'webpack', 'css_frameworks', 'mobile_development'
                ]
            },
            'Cybersecurity Analyst': {
                'essential': [
                    'network_security', 'penetration_testing', 'risk_assessment', 
                    'security_tools', 'incident_response', 'vulnerability_assessment'
                ],
                'important': [
                    'python', 'linux', 'firewall', 'siem', 'ids_ips', 
                    'encryption', 'compliance', 'audit', 'forensics'
                ],
                'bonus': [
                    'cloud_security', 'container_security', 'devops', 
                    'scripting', 'malware_analysis', 'threat_intelligence'
                ]
            },
            'Cloud Engineer': {
                'essential': [
                    'aws', 'azure', 'gcp', 'cloud_computing', 'networking', 
                    'security', 'storage', 'databases'
                ],
                'important': [
                    'docker', 'kubernetes', 'terraform', 'ansible', 'ci_cd', 
                    'monitoring', 'load_balancing', 'auto_scaling'
                ],
                'bonus': [
                    'serverless', 'microservices', 'devops', 'python', 
                    'infrastructure_as_code', 'cost_optimization'
                ]
            },
            'DevOps Engineer': {
                'essential': [
                    'docker', 'kubernetes', 'ci_cd', 'linux', 'automation', 
                    'monitoring', 'infrastructure', 'deployment'
                ],
                'important': [
                    'jenkins', 'gitlab_ci', 'terraform', 'ansible', 'aws', 
                    'azure', 'scripting', 'system_administration'
                ],
                'bonus': [
                    'prometheus', 'grafana', 'elk_stack', 'security', 
                    'performance_tuning', 'troubleshooting', 'python'
                ]
            },
            'Researcher': {
                'essential': [
                    'research_methods', 'academic_writing', 'critical_thinking', 
                    'statistics', 'data_analysis', 'literature_review'
                ],
                'important': [
                    'python', 'r', 'latex', 'experiment_design', 
                    'hypothesis_testing', 'data_visualization', 'presentation'
                ],
                'bonus': [
                    'machine_learning', 'nlp', 'domain_expertise', 
                    'publication', 'peer_review', 'grant_writing'
                ]
            },
            'Product Manager': {
                'essential': [
                    'product_management', 'user_research', 'market_analysis', 
                    'roadmap_planning', 'stakeholder_management'
                ],
                'important': [
                    'agile', 'scrum', 'analytics', 'communication', 
                    'leadership', 'prioritization', 'user_stories'
                ],
                'bonus': [
                    'technical_skills', 'business_acumen', 'design_thinking', 
                    'metrics', 'a_b_testing', 'growth_hacking'
                ]
            },
            'UI/UX Engineer': {
                'essential': [
                    'user_experience', 'user_interface', 'design_thinking', 
                    'prototyping', 'user_research', 'visual_design'
                ],
                'important': [
                    'figma', 'adobe_xd', 'sketch', 'html', 'css', 'javascript', 
                    'usability_testing', 'interaction_design'
                ],
                'bonus': [
                    'motion_design', 'accessibility', 'responsive_design', 
                    'design_systems', 'front_end_development', 'psychology'
                ]
            }
        }
        
        # Learning resources database
        self.learning_resources = {
            'python': [
                {'platform': 'Coursera', 'course': 'Python for Everybody', 'duration': '3 months'},
                {'platform': 'edX', 'course': 'Introduction to Computer Science', 'duration': '6 months'},
                {'platform': 'Udemy', 'course': 'Complete Python Bootcamp', 'duration': '2 months'}
            ],
            'machine_learning': [
                {'platform': 'Coursera', 'course': 'Machine Learning by Andrew Ng', 'duration': '3 months'},
                {'platform': 'Fast.ai', 'course': 'Practical Deep Learning', 'duration': '2 months'},
                {'platform': 'Udacity', 'course': 'Machine Learning Nanodegree', 'duration': '4 months'}
            ],
            'aws': [
                {'platform': 'AWS Training', 'course': 'AWS Cloud Practitioner', 'duration': '1 month'},
                {'platform': 'Udemy', 'course': 'AWS Certified Solutions Architect', 'duration': '2 months'},
                {'platform': 'A Cloud Guru', 'course': 'AWS Fundamentals', 'duration': '1 month'}
            ],
            'docker': [
                {'platform': 'Docker Training', 'course': 'Docker Mastery', 'duration': '1 month'},
                {'platform': 'KodeKloud', 'course': 'Docker for Beginners', 'duration': '2 weeks'},
                {'platform': 'Udemy', 'course': 'Docker & Kubernetes', 'duration': '3 months'}
            ],
            'react': [
                {'platform': 'React Documentation', 'course': 'Official React Tutorial', 'duration': '2 weeks'},
                {'platform': 'Udemy', 'course': 'Modern React with Redux', 'duration': '2 months'},
                {'platform': 'Scrimba', 'course': 'Learn React', 'duration': '1 month'}
            ]
        }
    
    def normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize skill names to standard format"""
        normalized = []
        skill_mapping = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine_learning',
            'ai': 'artificial_intelligence',
            'devops': 'devops',
            'ci/cd': 'ci_cd',
            'ui/ux': 'ui_ux_design',
            'sql': 'sql',
            'nosql': 'nosql',
            'git': 'git',
            'github': 'git',
            'aws': 'aws',
            'azure': 'azure',
            'gcp': 'gcp'
        }
        
        for skill in skills:
            skill_lower = skill.lower().strip().replace(' ', '_').replace('-', '_')
            normalized_skill = skill_mapping.get(skill_lower, skill_lower)
            if normalized_skill and len(normalized_skill) > 1:
                normalized.append(normalized_skill)
        
        return list(set(normalized))  # Remove duplicates
    
    def calculate_skill_similarity(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Calculate similarity between user skills and required skills using embeddings"""
        if not user_skills or not required_skills:
            return 0.0
        
        # Create embeddings
        user_embeddings = self.embedding_model.encode(user_skills)
        required_embeddings = self.embedding_model.encode(required_skills)
        
        # Calculate cosine similarity matrix
        similarity_matrix = np.dot(user_embeddings, required_embeddings.T)
        
        # For each required skill, find the best matching user skill
        max_similarities = np.max(similarity_matrix, axis=0)
        
        # Return average similarity
        return np.mean(max_similarities)
    
    def identify_skill_gaps(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """Identify missing and weak skills for target career"""
        if target_career not in self.career_skill_requirements:
            raise ValueError(f"Career '{target_career}' not found in database")
        
        user_skills_normalized = self.normalize_skills(user_skills)
        career_requirements = self.career_skill_requirements[target_career]
        
        # Flatten all required skills with priorities
        all_required = []
        skill_priorities = {}
        
        for priority, skills in career_requirements.items():
            for skill in skills:
                all_required.append(skill)
                if priority == 'essential':
                    skill_priorities[skill] = 3
                elif priority == 'important':
                    skill_priorities[skill] = 2
                else:  # bonus
                    skill_priorities[skill] = 1
        
        # Find missing skills
        missing_skills = []
        weak_skills = []
        
        for skill in all_required:
            if skill not in user_skills_normalized:
                # Check if there are similar skills
                similar_found = False
                for user_skill in user_skills_normalized:
                    similarity = self.calculate_skill_similarity([user_skill], [skill])
                    if similarity > 0.7:  # High similarity threshold
                        weak_skills.append(skill)
                        similar_found = True
                        break
                
                if not similar_found:
                    missing_skills.append(skill)
        
        # Calculate skill scores
        current_skill_score = len(user_skills_normalized) / len(all_required) if all_required else 0
        target_skill_score = 1.0
        gap_percentage = (target_skill_score - current_skill_score) * 100
        
        # Prioritize learning order (essential first, then important, then bonus)
        priority_order = sorted(
            missing_skills + weak_skills,
            key=lambda x: (-skill_priorities.get(x, 0), x)
        )
        
        return {
            "missing_skills": missing_skills,
            "weak_skills": weak_skills,
            "priority_learning_order": priority_order[:10],  # Top 10 priorities
            "current_skill_score": round(current_skill_score, 3),
            "target_skill_score": target_skill_score,
            "gap_percentage": round(gap_percentage, 1)
        }
    
    def recommend_learning_resources(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Recommend learning resources for given skills"""
        recommendations = []
        
        for skill in skills:
            if skill in self.learning_resources:
                resources = self.learning_resources[skill]
                recommendations.extend([
                    {
                        "skill": skill,
                        "platform": resource["platform"],
                        "course": resource["course"],
                        "duration": resource["duration"]
                    }
                    for resource in resources[:2]  # Top 2 resources per skill
                ])
        
        return recommendations
    
    def recommend_projects(self, target_career: str, user_skills: List[str]) -> List[str]:
        """Recommend project ideas based on career and current skills"""
        project_database = {
            'Data Scientist': [
                "Customer churn prediction using machine learning",
                "Sentiment analysis on social media data",
                "Stock price prediction with time series analysis",
                "Recommendation system for e-commerce",
                "COVID-19 data visualization and analysis"
            ],
            'ML Engineer': [
                "Deploy ML model as REST API using FastAPI",
                "Build an image classification pipeline with MLOps",
                "Create a real-time fraud detection system",
                "Develop a chatbot with NLP capabilities",
                "Build an automated ML pipeline with Airflow"
            ],
            'Software Developer': [
                "Build a scalable microservices architecture",
                "Create a real-time collaboration tool",
                "Develop a performance monitoring system",
                "Build a secure authentication system",
                "Create a distributed caching solution"
            ],
            'Full Stack Developer': [
                "Build a social media platform with React and Node.js",
                "Create an e-commerce website with payment integration",
                "Develop a real-time chat application",
                "Build a project management tool",
                "Create a video streaming platform"
            ],
            'Cybersecurity Analyst': [
                "Build a network intrusion detection system",
                "Create a vulnerability scanner for web applications",
                "Develop a security incident response dashboard",
                "Build a password strength analyzer",
                "Create a secure file sharing system"
            ],
            'Cloud Engineer': [
                "Deploy a multi-tier application on AWS",
                "Build an auto-scaling web application",
                "Create a serverless data processing pipeline",
                "Implement infrastructure as code with Terraform",
                "Build a container orchestration system"
            ],
            'DevOps Engineer': [
                "Build a complete CI/CD pipeline",
                "Create an automated testing framework",
                "Develop a container monitoring system",
                "Build an infrastructure automation tool",
                "Create a deployment orchestration platform"
            ],
            'Researcher': [
                "Conduct a comprehensive literature review",
                "Design and execute an experimental study",
                "Build a data collection and analysis framework",
                "Create a research paper with reproducible results",
                "Develop a novel algorithm for a specific problem"
            ],
            'Product Manager': [
                "Create a product roadmap for a mobile app",
                "Conduct user research and persona development",
                "Design an MVP for a SaaS product",
                "Build a competitive analysis framework",
                "Create a go-to-market strategy"
            ],
            'UI/UX Engineer': [
                "Design a mobile app UI/UX from scratch",
                "Create a design system for a web application",
                "Conduct usability testing and redesign",
                "Build an interactive prototype",
                "Design an accessible website"
            ]
        }
        
        career_projects = project_database.get(target_career, [])
        
        # Filter projects based on current skills (prefer projects that use existing skills)
        scored_projects = []
        for project in career_projects:
            score = 0
            for skill in user_skills:
                if skill.lower() in project.lower():
                    score += 1
            scored_projects.append((project, score))
        
        # Sort by score and return top 5
        scored_projects.sort(key=lambda x: x[1], reverse=True)
        return [project for project, _ in scored_projects[:5]]
    
    def analyze_skill_gap(self, user_skills: List[str], target_career: str) -> Dict[str, Any]:
        """Complete skill gap analysis"""
        # Identify gaps
        gap_analysis = self.identify_skill_gaps(user_skills, target_career)
        
        # Recommend courses
        priority_skills = gap_analysis["priority_learning_order"][:5]
        course_recommendations = self.recommend_learning_resources(priority_skills)
        
        # Recommend projects
        project_recommendations = self.recommend_projects(target_career, user_skills)
        
        # Recommend certifications
        cert_recommendations = self.recommend_certifications(target_career, gap_analysis["missing_skills"])
        
        return {
            **gap_analysis,
            "recommended_courses": course_recommendations,
            "recommended_certifications": cert_recommendations,
            "recommended_projects": project_recommendations
        }
    
    def recommend_certifications(self, target_career: str, missing_skills: List[str]) -> List[str]:
        """Recommend certifications based on career and missing skills"""
        cert_database = {
            'Data Scientist': [
                "Google Data Analytics Certificate",
                "IBM Data Science Professional Certificate",
                "Microsoft Azure Data Scientist Associate",
                "AWS Certified Machine Learning"
            ],
            'ML Engineer': [
                "TensorFlow Developer Certificate",
                "AWS Certified Machine Learning",
                "Google Cloud ML Engineer",
                "Microsoft Azure AI Engineer"
            ],
            'Software Developer': [
                "AWS Certified Developer",
                "Oracle Java Programmer",
                "Microsoft Azure Developer",
                "Google Cloud Developer"
            ],
            'Full Stack Developer': [
                "AWS Certified Developer",
                "MongoDB Certified Developer",
                "React Certification",
                "Google Cloud Developer"
            ],
            'Cybersecurity Analyst': [
                "CompTIA Security+",
                "Certified Ethical Hacker (CEH)",
                "CISSP",
                "AWS Certified Security"
            ],
            'Cloud Engineer': [
                "AWS Solutions Architect",
                "Azure Administrator Associate",
                "Google Cloud Professional Architect",
                "Certified Kubernetes Administrator"
            ],
            'DevOps Engineer': [
                "AWS DevOps Engineer",
                "Certified Kubernetes Administrator",
                "Docker Certified Associate",
                "Azure DevOps Engineer"
            ],
            'Researcher': [
                "Research Methods Certification",
                "Statistical Analysis Certificate",
                "Academic Writing Certificate",
                "Domain-specific certifications"
            ],
            'Product Manager': [
                "Google Project Management Certificate",
                "Scrum Master Certification",
                "Product Management Certificate",
                "Agile Certification"
            ],
            'UI/UX Engineer': [
                "Google UX Design Certificate",
                "Adobe Certified Expert",
                "Figma Certification",
                "Interaction Design Foundation"
            ]
        }
        
        return cert_database.get(target_career, [])[:3]
