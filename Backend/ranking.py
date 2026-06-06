from embedding_engine import generate_embedding
from similarity import calculate_similarity


def rank_resumes(job_description, resumes):
    ranked_candidates = []

    job_embedding = generate_embedding(job_description)

    for candidate_name, resume_text in resumes.items():

        resume_embedding = generate_embedding(
            resume_text
        )

        score = calculate_similarity(
            resume_embedding,
            job_embedding
        )

        ranked_candidates.append({
            "candidate": candidate_name,
            "score": round(float(score*100),2)
        })

    ranked_candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_candidates