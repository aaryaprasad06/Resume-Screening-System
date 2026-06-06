from fastapi import FastAPI
from models import RankingRequest
from ranking import rank_resumes

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Resume Screening API Running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/rank-resumes")
def rank_candidates(request: RankingRequest):

    results = rank_resumes(
        request.job_description,
        request.resumes
    )

    return {
        "rankings": results
    }