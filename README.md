🚀 HireMind AI

AI-powered resume screening system that ranks candidates, extracts insights, and generates interview questions in seconds.

Turn raw resumes into structured hiring intelligence using LLMs.

✨ Overview

HireMind AI helps recruiters instantly evaluate candidates against a job description using AI.
It analyzes resumes, compares them with role requirements, and produces clear hiring insights + rankings.

Think of it as an AI recruiter that never gets tired.

🎯 Key Features
📄 Smart Resume Processing
Upload single or multiple PDF resumes
Automatic text extraction from resumes
Clean parsing for LLM analysis
🧠 AI Candidate Intelligence
Match score (0–100) against job description
Strengths & weaknesses breakdown
Skill relevance detection
🏆 Candidate Ranking System
Automatic sorting by fit score
Compare multiple candidates instantly
Dynamic re-ranking with new job descriptions
💬 Interview Assistant
AI-generated technical + behavioral questions
Personalized per candidate profile
Role-specific questioning strategy
🧰 Tech Stack
Layer	Technology
Frontend	React + Vite + Axios
Backend	FastAPI (Python)
AI Engine	Groq API (Llama 3.3 70B)
PDF Parsing	PyPDF2
Styling	Custom CSS (Glassmorphism UI)
📁 Project Structure
hiremind/
├── backend/
│   ├── app.py              # API routes (FastAPI)
│   ├── llm_analysis.py     # AI scoring logic (Groq)
│   ├── resume_parser.py    # PDF → text extraction
│   ├── requirements.txt
│   └── uploads/            # Temporary storage (git ignored)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
│
├── .gitignore
└── README.md

⚡ Getting Started
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/hiremind.git
cd hiremind
2️⃣ Backend Setup
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_api_key_here

Run backend:

uvicorn app:app --reload

📍 Backend runs at: http://localhost:8000

3️⃣ Frontend Setup
cd frontend
npm install
npm run dev

📍 Frontend runs at: http://localhost:5173

🔌 API Endpoints
🟢 Health Check
GET /health
📤 Upload Resume(s)
POST /upload-resumes

Form Data:

files → PDF resumes
🧠 Rank Candidates
POST /rank-candidates

Request:

{
  "job_description": "We are looking for a Python developer...",
  "resumes": [
    { "filename": "john.pdf", "text": "..." }
  ]
}

Response:

Ranked candidates (highest match first)
Score + insights + interview questions
🌐 Deployment
⚡ Frontend (Vercel)
Push repo to GitHub
Import into Vercel
Set root directory → frontend
Deploy 🚀
⚡ Backend (Railway)
Deploy repo on Railway
Set root → backend

Add env variable:

GROQ_API_KEY
Done 🚀
📸 Preview

Add your screenshot here for maximum impact

/screenshot.png
💡 Why HireMind?
⚡ Faster hiring decisions
🧠 AI-powered resume understanding
📊 Objective candidate scoring
🔍 Eliminates manual screening bias
💼 Scales hiring pipelines instantly
🤝 Contributing

Ideas, improvements, and PRs are welcome.

If you're building something cool on top of this — feel free to fork it.

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/hiremind?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/hiremind?style=social)
![License](https://img.shields.io/github/license/YOUR_USERNAME/hiremind)
