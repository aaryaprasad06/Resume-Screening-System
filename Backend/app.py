from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import re
import json

from resume_parser import extract_text_from_pdf
from llm_analysis import analyze_candidate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "HireMind Resume Screening API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ── Helpers ──────────────────────────────────────────────────────────────────

def safe_parse_llm_json(raw) -> dict:
    """
    Robustly parse the JSON that analyze_candidate returns.
    Handles:
      - already a dict
      - plain JSON string
      - JSON wrapped in ```json ... ``` fences
      - stray leading/trailing text around the JSON object
    Falls back to a zeroed-out dict so the app never crashes.
    """
    if isinstance(raw, dict):
        return raw

    if not isinstance(raw, str):
        raw = str(raw)

    # Strip markdown code fences if present
    raw = re.sub(r"```(?:json)?\s*", "", raw).strip()

    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to extract the first {...} block
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # Total fallback
    return {
        "match_score": 0,
        "summary": raw[:300] if raw else "Could not parse analysis.",
        "strengths": [],
        "weaknesses": [],
        "interview_questions": [],
    }


# ── Upload multiple resumes ───────────────────────────────────────────────────

@app.post("/upload-resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Accept one or more PDF resumes.
    Returns [{filename, text}, ...].
    """
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        content = await file.read()
        with open(file_path, "wb") as buf:
            buf.write(content)

        text = extract_text_from_pdf(file_path)
        results.append({"filename": file.filename, "text": text or ""})

    return {"resumes": results}


# ── Rank all candidates ───────────────────────────────────────────────────────

class BulkAnalysisRequest(BaseModel):
    job_description: str
    resumes: List[dict]   # [{filename, text}, ...]


@app.post("/rank-candidates")
def rank_candidates(request: BulkAnalysisRequest):
    """
    Score every resume with the LLM, then return them sorted best-first.

    analyze_candidate must return a JSON string (or dict) shaped like:
    {
      "match_score": 87,          <- integer 0-100
      "summary": "...",           <- one-sentence summary
      "strengths": ["..."],       <- list of strings
      "weaknesses": ["..."],      <- list of strings
      "interview_questions": ["..."]
    }
    """
    results = []

    for resume in request.resumes:
        raw = analyze_candidate(resume["text"], request.job_description)
        data = safe_parse_llm_json(raw)

        # Ensure match_score is a plain int in [0, 100]
        try:
            score = int(data.get("match_score", 0))
            score = max(0, min(100, score))
        except (TypeError, ValueError):
            score = 0

        results.append({
            "filename": resume["filename"],
            "match_score": score,
            "summary": str(data.get("summary", "")),
            "strengths": list(data.get("strengths", [])),
            "weaknesses": list(data.get("weaknesses", [])),
            "interview_questions": list(data.get("interview_questions", [])),
        })

    # Sort highest score first — this is the order the frontend displays
    results.sort(key=lambda x: x["match_score"], reverse=True)

    return {"candidates": results}