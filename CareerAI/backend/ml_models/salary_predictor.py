import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from typing import Dict, Any, Tuple

class SalaryPredictor:
    def __init__(self):
        self.entry_model = None
        self.experienced_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
        # Market data for different careers (base salaries in USD)
        self.market_data = {
            'Data Scientist': {'entry': 85000, 'experienced': 130000, 'growth': 0.08},
            'ML Engineer': {'entry': 95000, 'experienced': 150000, 'growth': 0.10},
            'Software Developer': {'entry': 75000, 'experienced': 120000, 'growth': 0.07},
            'Full Stack Developer': {'entry': 80000, 'experienced': 125000, 'growth': 0.08},
            'Cybersecurity Analyst': {'entry': 70000, 'experienced': 115000, 'growth': 0.09},
            'Cloud Engineer': {'entry': 85000, 'experienced': 135000, 'growth': 0.09},
            'DevOps Engineer': {'entry': 90000, 'experienced': 140000, 'growth': 0.09},
            'Researcher': {'entry': 65000, 'experienced': 110000, 'growth': 0.06},
            'Product Manager': {'entry': 80000, 'experienced': 140000, 'growth': 0.08},
            'UI/UX Engineer': {'entry': 70000, 'experienced': 110000, 'growth': 0.07}
        }
        
        self.load_or_train_models()
    
    def load_or_train_models(self):
        """Load existing models or train with sample data"""
        entry_model_path = "backend/ml_models/entry_salary_model.pkl"
        experienced_model_path = "backend/ml_models/experienced_salary_model.pkl"
        
        if os.path.exists(entry_model_path) and os.path.exists(experienced_model_path):
            try:
                self.entry_model = joblib.load(entry_model_path)
                self.experienced_model = joblib.load(experienced_model_path)
                print("✅ Salary prediction models loaded successfully")
                return
            except Exception as e:
                print(f"⚠️ Error loading salary models: {e}")
        
        # Train with sample data if no models exist
        self.train_sample_models()
    
    def create_sample_dataset(self) -> pd.DataFrame:
        """Create a sample dataset for salary prediction"""
        np.random.seed(42)
        n_samples = 1000
        
        data = []
        careers = list(self.market_data.keys())
        
        for _ in range(n_samples):
            career = np.random.choice(careers)
            career_data = self.market_data[career]
            
            # Generate features
            cgpa = np.random.uniform(6.0, 10.0)
            n_technical_skills = np.random.randint(3, 15)
            n_soft_skills = np.random.randint(2, 8)
            n_certifications = np.random.randint(0, 5)
            n_internships = np.random.randint(0, 3)
            github_score = np.random.uniform(0.1, 1.0)
            
            # University tier effect (1-5, where 5 is best)
            university_tier = np.random.randint(1, 6)
            
            # Location factor (major tech hub vs other)
            location_factor = np.random.choice([1.2, 1.0, 0.9], p=[0.3, 0.5, 0.2])
            
            # Calculate base salary with variations
            entry_base = career_data['entry']
            experienced_base = career_data['experienced']
            
            # Add individual factors
            cgpa_factor = 0.8 + (cgpa / 10.0) * 0.4  # 0.8 to 1.2
            skills_factor = 0.9 + (n_technical_skills / 15.0) * 0.3  # 0.9 to 1.2
            github_factor = 0.9 + github_score * 0.2  # 0.9 to 1.1
            university_factor = 0.85 + (university_tier / 5.0) * 0.3  # 0.85 to 1.15
            
            entry_salary = (entry_base * cgpa_factor * skills_factor * 
                          github_factor * university_factor * location_factor)
            
            experienced_salary = (experienced_base * cgpa_factor * skills_factor * 
                               github_factor * university_factor * location_factor)
            
            # Add some noise
            entry_salary += np.random.normal(0, 5000)
            experienced_salary += np.random.normal(0, 8000)
            
            # Ensure positive values
            entry_salary = max(40000, entry_salary)
            experienced_salary = max(60000, experienced_salary)
            
            data.append({
                'career': career,
                'cgpa': cgpa,
                'n_technical_skills': n_technical_skills,
                'n_soft_skills': n_soft_skills,
                'n_certifications': n_certifications,
                'n_internships': n_internships,
                'github_score': github_score,
                'university_tier': university_tier,
                'location_factor': location_factor,
                'entry_salary': entry_salary,
                'experienced_salary': experienced_salary
            })
        
        return pd.DataFrame(data)
    
    def train_sample_models(self):
        """Train salary prediction models with sample data"""
        print("🔄 Training salary prediction models...")
        
        # Create sample dataset
        df = self.create_sample_dataset()
        
        # Prepare features
        feature_columns = [
            'cgpa', 'n_technical_skills', 'n_soft_skills', 
            'n_certifications', 'n_internships', 'github_score',
            'university_tier', 'location_factor'
        ]
        
        # Add career encoding
        career_dummies = pd.get_dummies(df['career'], prefix='career')
        X = pd.concat([df[feature_columns], career_dummies], axis=1)
        
        self.feature_names = X.columns.tolist()
        
        # Targets
        y_entry = df['entry_salary']
        y_experienced = df['experienced_salary']
        
        # Split data
        X_train, X_test, y_entry_train, y_entry_test, y_exp_train, y_exp_test = train_test_split(
            X, y_entry, y_experienced, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train entry-level model
        self.entry_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.entry_model.fit(X_train_scaled, y_entry_train)
        
        # Train experienced model
        self.experienced_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.experienced_model.fit(X_train_scaled, y_exp_train)
        
        # Evaluate models
        entry_pred = self.entry_model.predict(X_test_scaled)
        exp_pred = self.experienced_model.predict(X_test_scaled)
        
        entry_mae = mean_absolute_error(y_entry_test, entry_pred)
        exp_mae = mean_absolute_error(y_exp_test, exp_pred)
        
        entry_r2 = r2_score(y_entry_test, entry_pred)
        exp_r2 = r2_score(y_exp_test, exp_pred)
        
        print(f"✅ Entry-level model - MAE: ${entry_mae:,.0f}, R²: {entry_r2:.3f}")
        print(f"✅ Experienced model - MAE: ${exp_mae:,.0f}, R²: {exp_r2:.3f}")
        
        # Save models
        os.makedirs("backend/ml_models", exist_ok=True)
        joblib.dump(self.entry_model, "backend/ml_models/entry_salary_model.pkl")
        joblib.dump(self.experienced_model, "backend/ml_models/experienced_salary_model.pkl")
        joblib.dump(self.scaler, "backend/ml_models/salary_scaler.pkl")
        joblib.dump(self.feature_names, "backend/ml_models/salary_feature_names.pkl")
    
    def extract_features(self, profile_data: Dict[str, Any], career: str, github_data: Dict[str, Any] = None) -> np.ndarray:
        """Extract features for salary prediction"""
        features = {}
        
        # Basic features
        features['cgpa'] = profile_data.get('cgpa', 7.0)
        features['n_technical_skills'] = len(profile_data.get('technical_skills', []))
        features['n_soft_skills'] = len(profile_data.get('soft_skills', []))
        features['n_certifications'] = len(profile_data.get('certifications', []))
        features['n_internships'] = len(profile_data.get('internships', []))
        features['github_score'] = github_data.get('overall_github_score', 0.5) if github_data else 0.5
        
        # Assumed features (would need user input in production)
        features['university_tier'] = 3  # Default to mid-tier
        features['location_factor'] = 1.0  # Default to average location
        
        # Career encoding
        for career_name in self.market_data.keys():
            features[f'career_{career_name}'] = 1.0 if career_name == career else 0.0
        
        # Convert to array in correct order
        feature_array = []
        for feature_name in self.feature_names:
            feature_array.append(features.get(feature_name, 0.0))
        
        return np.array(feature_array).reshape(1, -1)
    
    def predict(self, profile_data: Dict[str, Any], career: str, github_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Predict salary for given profile and career"""
        if self.entry_model is None or self.experienced_model is None:
            raise ValueError("Models not trained or loaded")
        
        # Extract features
        features = self.extract_features(profile_data, career, github_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        entry_salary = self.entry_model.predict(features_scaled)[0]
        experienced_salary = self.experienced_model.predict(features_scaled)[0]
        
        # Calculate 5-year projection
        growth_rate = self.market_data.get(career, {}).get('growth', 0.08)
        five_year_projection = entry_salary * ((1 + growth_rate) ** 5)
        
        # Market demand score based on growth rate and salary potential
        market_demand_score = min(1.0, (growth_rate / 0.12) * 0.6 + (experienced_salary / 150000) * 0.4)
        
        return {
            "entry_level": round(entry_salary, 0),
            "five_year": round(five_year_projection, 0),
            "experienced_level": round(experienced_salary, 0),
            "growth_rate": growth_rate,
            "market_demand_score": round(market_demand_score, 3)
        }
