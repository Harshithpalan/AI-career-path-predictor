# CareerAI – Intelligent Career Path Prediction & Skill Gap Analyzer

A production-ready AI platform that predicts the best career path for students based on their skills, academic performance, GitHub activity, and more.

## 🎯 Features

- **Career Path Prediction**: AI-powered classification into 10+ career tracks
- **Salary Prediction**: Entry-level and 5-year salary projections
- **Skill Gap Analysis**: Identify missing and weak skills for target careers
- **Personalized Roadmap**: 3, 6, and 12-month development plans
- **Job Readiness Score**: Comprehensive 0-100 scoring system
- **Resume Improvement Suggestions**: ATS-optimized recommendations
- **GitHub Intelligence**: Analyze code quality, consistency, and tech stack alignment

## 🏗️ Architecture

```
CareerAI/
├── backend/          # FastAPI REST API
├── frontend/         # React/Next.js Dashboard
├── ml-models/        # ML training and inference
├── database/         # PostgreSQL schemas
├── docker/           # Docker configurations
└── docs/            # Documentation
```

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Database Setup
```bash
cd database
docker-compose up -d
```

## 📊 Tech Stack

- **Frontend**: React, Next.js, TailwindCSS, Chart.js
- **Backend**: FastAPI, Python, PostgreSQL
- **ML/AI**: Scikit-learn, XGBoost, TensorFlow, OpenAI API
- **Infrastructure**: Docker, AWS/Vercel

## 🔧 API Endpoints

- `POST /api/predict-career` - Career prediction
- `POST /api/analyze-github` - GitHub profile analysis
- `POST /api/skill-gap` - Skill gap analysis
- `POST /api/generate-roadmap` - Personalized roadmap

## 📈 Models

- **Career Classification**: Multi-class classifier (Random Forest, XGBoost, Neural Network)
- **Salary Prediction**: Regression model with market data integration
- **Skill Embedding**: Vector-based skill comparison engine

## 🔒 Security

- JWT Authentication
- GitHub OAuth integration
- API rate limiting
- Input validation and sanitization

## 📚 Documentation

See `/docs` folder for:
- API documentation
- Model training guides
- Deployment instructions
- Architecture diagrams

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details
