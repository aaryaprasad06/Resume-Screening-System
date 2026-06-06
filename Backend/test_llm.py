from llm_analysis import analyze_candidate

resume = """
Python developer with TensorFlow,
Machine Learning and Deep Learning.
"""

job = """
Looking for ML engineer with
TensorFlow and MLOps experience.
"""

result = analyze_candidate(
    resume,
    job
)

print(result)