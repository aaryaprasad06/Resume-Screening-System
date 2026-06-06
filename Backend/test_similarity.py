from embedding_engine import generate_embedding
from similarity import calculate_similarity

resume_text = """
Python developer with machine learning
experience using TensorFlow and PyTorch
"""

job_text = """
Looking for a Python machine learning engineer
with experience in deep learning
"""

resume_embedding = generate_embedding(resume_text)
job_embedding = generate_embedding(job_text)

score = calculate_similarity(
    resume_embedding,
    job_embedding
)

print(f"Similarity Score: {score:.4f}")