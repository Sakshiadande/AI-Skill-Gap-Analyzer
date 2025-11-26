from skill_extraction import load_skills_list, extract_skills_keyword, extract_skills_spacy

resume_text = "Experienced in Python, machine learning, deep learning, SQL and data structures."
jd_text = "Looking for a candidate with Python, NLP, machine learning, communication skills and SQL."

skills_list = load_skills_list()

print("Resume skills:", extract_skills_keyword(resume_text, skills_list))
print("JD skills:", extract_skills_keyword(jd_text, skills_list))
