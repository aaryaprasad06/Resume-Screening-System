from embedding_engine import generate_embedding

resume_text = "Python developer with machine learning skills"

job_text = "Looking for a machine learning engineer skilled in Python"

resume_embedding = generate_embedding(resume_text)

job_embedding = generate_embedding(job_text)

print(len(resume_embedding))
print(len(job_embedding))