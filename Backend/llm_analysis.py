from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_candidate(resume_text: str, job_description: str) -> dict:

    prompt = f"""You are a resume screening assistant. Compare the resume below against the job description.

Respond with ONLY a JSON object — no markdown, no code fences, no explanation, no extra text.
The JSON must follow this exact shape:

{{
  "match_score": <integer between 0 and 100 reflecting overall fit>,
  "summary": "<one sentence, maximum 15 words>",
  "strengths": [
    "<specific strength>",
    "<specific strength>",
    "<specific strength>"
  ],
  "weaknesses": [
    "<specific weakness or gap>",
    "<specific weakness or gap>"
  ],
  "interview_questions": [
    "<tailored question>",
    "<tailored question>",
    "<tailored question>"
  ]
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a JSON-only API. You never write prose, markdown, "
                    "or explanations. Every response is a single valid JSON object."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,       # lower = more deterministic / less creative formatting
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()

    # Strip accidental markdown fences the model sometimes adds anyway
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Last resort: pull the first {...} block out of whatever was returned
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Total fallback so the app never crashes
        return {
            "match_score": 0,
            "summary": "Could not parse LLM response.",
            "strengths": [],
            "weaknesses": [],
            "interview_questions": []
        }