from resume_parser import extract_text_from_pdf

resume_text = extract_text_from_pdf(
    "../Sample_data/sample_resume.pdf"
)

print(resume_text)