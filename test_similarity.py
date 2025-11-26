from similarity import compare_skills

resume_skills = ["python", "deep learning", "sql", "data structures"]
jd_skills = ["python", "machine learning", "communication", "sql"]

results, _ = compare_skills(resume_skills, jd_skills)

for r in results:
    print(r)
