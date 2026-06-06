from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_candidate(
    resume_text,
    job_description
):

    prompt = f"""
    Compare the resume with the job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Provide:

    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. Interview Questions
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content