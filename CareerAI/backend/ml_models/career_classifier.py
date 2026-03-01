import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
import joblib
from typing import Dict, List, Tuple, Any
import os

class CareerClassifier:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = []
        self.career_categories = [
            'Data Scientist',
            'ML Engineer', 
            'Software Developer',
            'Full Stack Developer',
            'Cybersecurity Analyst',
            'Cloud Engineer',
            'DevOps Engineer',
            'Researcher',
            'Product Manager',
            'UI/UX Engineer'
        ]
        
        # Skill embeddings for different careers
        self.career_skill_weights = {
            'Data Scientist': {
                'python': 0.9, 'machine_learning': 0.95, 'statistics': 0.9, 
                'sql': 0.8, 'data_analysis': 0.9, 'tensorflow': 0.8, 'pandas': 0.85
            },
            'ML Engineer': {
                'python': 0.9, 'machine_learning': 0.95, 'deep_learning': 0.9,
                'tensorflow': 0.9, 'pytorch': 0.85, 'mlops': 0.8, 'docker': 0.7
            },
            'Software Developer': {
                'python': 0.8, 'java': 0.8, 'javascript': 0.7, 'algorithms': 0.9,
                'data_structures': 0.9, 'oop': 0.8, 'git': 0.7
            },
            'Full Stack Developer': {
                'javascript': 0.9, 'react': 0.85, 'nodejs': 0.8, 'html': 0.9,
                'css': 0.9, 'mongodb': 0.7, 'express': 0.75, 'api_design': 0.8
            },
            'Cybersecurity Analyst': {
                'network_security': 0.9, 'penetration_testing': 0.85, 'python': 0.7,
                'linux': 0.8, 'firewall': 0.8, 'siem': 0.75, 'risk_assessment': 0.85
            },
            'Cloud Engineer': {
                'aws': 0.9, 'azure': 0.85, 'gcp': 0.8, 'docker': 0.85,
                'kubernetes': 0.9, 'terraform': 0.8, 'devops': 0.75
            },
            'DevOps Engineer': {
                'docker': 0.9, 'kubernetes': 0.9, 'ci_cd': 0.95, 'jenkins': 0.8,
                'ansible': 0.8, 'terraform': 0.8, 'linux': 0.85
            },
            'Researcher': {
                'python': 0.8, 'statistics': 0.9, 'research_methods': 0.95,
                'academic_writing': 0.9, 'data_analysis': 0.85, 'critical_thinking': 0.9
            },
            'Product Manager': {
                'product_management': 0.95, 'agile': 0.8, 'scrum': 0.8,
                'analytics': 0.75, 'communication': 0.9, 'leadership': 0.85
            },
            'UI/UX Engineer': {
                'figma': 0.9, 'adobe_xd': 0.85, 'user_research': 0.9,
                'prototyping': 0.85, 'html': 0.7, 'css': 0.7, 'javascript': 0.6
            }
        }
        
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train with sample data"""
        model_path = "backend/ml_models/career_model.pkl"
        
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print("✅ Career classification model loaded successfully")
                return
            except Exception as e:
                print(f"⚠️ Error loading model: {e}")
        
        # Train with sample data if no model exists
        self.train_sample_model()
    
    def create_sample_dataset(self) -> pd.DataFrame:
        """Create a sample dataset for training"""
        np.random.seed(42)
        n_samples = 1000
        
        data = []
        for _ in range(n_samples):
            career = np.random.choice(self.career_categories)
            
            # Generate random features
            cgpa = np.random.uniform(6.0, 10.0)
            n_technical_skills = np.random.randint(3, 15)
            n_soft_skills = np.random.randint(2, 8)
            n_certifications = np.random.randint(0, 5)
            n_internships = np.random.randint(0, 3)
            n_projects = np.random.randint(1, 10)
            
            # GitHub metrics
            github_score = np.random.uniform(0.1, 1.0)
            commit_frequency = np.random.uniform(0.1, 1.0)
            
            # Career-specific skill alignment
            career_skills = self.career_skill_weights[career]
            skill_alignment = np.random.uniform(0.3, 1.0)
            
            data.append({
                'cgpa': cgpa,
                'n_technical_skills': n_technical_skills,
                'n_soft_skills': n_soft_skills,
                'n_certifications': n_certifications,
                'n_internships': n_internships,
                'n_projects': n_projects,
                'github_score': github_score,
                'commit_frequency': commit_frequency,
                'skill_alignment': skill_alignment,
                'career': career
            })
        
        return pd.DataFrame(data)
    
    def train_sample_model(self):
        """Train model with sample data"""
        print("🔄 Training career classification model...")
        
        # Create sample dataset
        df = self.create_sample_dataset()
        
        # Prepare features and target
        feature_columns = [col for col in df.columns if col != 'career']
        X = df[feature_columns]
        y = df['career']
        
        # Encode target
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✅ Model trained with accuracy: {accuracy:.3f}")
        
        # Save model
        os.makedirs("backend/ml_models", exist_ok=True)
        joblib.dump(self.model, "backend/ml_models/career_model.pkl")
        joblib.dump(self.scaler, "backend/ml_models/scaler.pkl")
        joblib.dump(self.label_encoder, "backend/ml_models/label_encoder.pkl")
        
        self.feature_names = feature_columns
    
    def extract_features(self, profile_data: Dict[str, Any], github_data: Dict[str, Any] = None) -> np.ndarray:
        """Extract features from user profile and GitHub data"""
        features = []
        
        # Academic features
        features.append(profile_data.get('cgpa', 7.0) / 10.0)  # Normalize CGPA
        
        # Skills features
        technical_skills = profile_data.get('technical_skills', [])
        soft_skills = profile_data.get('soft_skills', [])
        features.append(len(technical_skills))
        features.append(len(soft_skills))
        
        # Experience features
        features.append(len(profile_data.get('certifications', [])))
        features.append(len(profile_data.get('internships', [])))
        features.append(len(profile_data.get('projects', [])))
        
        # GitHub features
        if github_data:
            features.append(github_data.get('overall_github_score', 0.5))
            features.append(github_data.get('commit_frequency', 0.5))
        else:
            features.append(0.5)  # Default values
            features.append(0.5)
        
        # Skill alignment score
        skill_alignment = self.calculate_skill_alignment(technical_skills)
        features.append(skill_alignment)
        
        return np.array(features).reshape(1, -1)
    
    def calculate_skill_alignment(self, user_skills: List[str]) -> float:
        """Calculate how well user skills align with different careers"""
        if not user_skills:
            return 0.5
        
        alignment_scores = []
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        for career, skill_weights in self.career_skill_weights.items():
            career_skills = list(skill_weights.keys())
            matches = sum(1 for skill in user_skills_lower if any(cs in skill for cs in career_skills))
            alignment = matches / len(career_skills) if career_skills else 0
            alignment_scores.append(alignment)
        
        return max(alignment_scores) if alignment_scores else 0.5
    
    def predict(self, profile_data: Dict[str, Any], github_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Predict career path for user"""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Extract features
        features = self.extract_features(profile_data, github_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction_proba = self.model.predict_proba(features_scaled)[0]
        predicted_class_idx = np.argmax(prediction_proba)
        predicted_career = self.label_encoder.inverse_transform([predicted_class_idx])[0]
        confidence = prediction_proba[predicted_class_idx]
        
        # Get top 3 alternatives
        top_3_indices = np.argsort(prediction_proba)[-3:][::-1][1:]  # Exclude top prediction
        alternatives = []
        for idx in top_3_indices:
            career = self.label_encoder.inverse_transform([idx])[0]
            score = prediction_proba[idx]
            alternatives.append({"career": career, "confidence": float(score)})
        
        # Feature importance
        feature_importance = dict(zip(self.feature_names, self.model.feature_importances_))
        
        return {
            "predicted_career": predicted_career,
            "confidence": float(confidence),
            "alternative_careers": alternatives,
            "feature_importance": feature_importance,
            "all_probabilities": dict(zip(self.label_encoder.classes_, prediction_proba.astype(float)))
        }
