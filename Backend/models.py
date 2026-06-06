from pydantic import BaseModel  # pydantic is used by fastapi to validate incoming data
from typing import Dict


class RankingRequest(BaseModel):
    job_description: str
    resumes: Dict[str, str]