from ranking import rank_resumes

job_description = """
Looking for a Python machine learning engineer
with TensorFlow and deep learning experience.
"""

resumes = {
    "Aarya":
    """
    Python developer with machine learning,
    TensorFlow and deep learning experience.
    """,

    "Rahul":
    """
    Java backend developer using Spring Boot.
    """,

    "Priya":
    """
    Machine learning engineer skilled in
    Python, TensorFlow and data science.
    """,

    "Arjun":
    """
    Civil engineer with AutoCAD and
    construction management experience.
    """,
    "Neha":
"""
Python, Machine Learning,
PyTorch, TensorFlow,
Computer Vision,
Deep Learning
"""
}

results = rank_resumes(
    job_description,
    resumes
)

for rank, candidate in enumerate(results, start=1):
    print(
        f"{rank}. "
        f"{candidate['candidate']} "
        f"({candidate['score']:.4f})"
    )