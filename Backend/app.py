from fastapi import FastAPI, UploadFile, File
from models import RankingRequest
from ranking import rank_resumes
from resume_parser import extract_text_from_pdf
import os

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

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    upload_dir = "../uploads"

    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        content = await file.read()

        buffer.write(content)

    extracted_text = extract_text_from_pdf(
        file_path
    )

    return {
        "filename": file.filename,
        "text_preview": extracted_text[:500]
    }