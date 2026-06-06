from fastapi import FastAPI

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