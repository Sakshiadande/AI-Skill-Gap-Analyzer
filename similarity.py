# similarity.py

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")  # lightweight & fast model

def generate_embeddings(skill_list):
    if not skill_list:
        return np.zeros((0, model.get_sentence_embedding_dimension()))
    return model.encode(skill_list, convert_to_numpy=True)

def compare_skills(resume_skills, jd_skills, threshold_match=0.80, threshold_weak=0.50):
    resume_embeddings = generate_embeddings(resume_skills)
    jd_embeddings = generate_embeddings(jd_skills)

    similarity_matrix = cosine_similarity(resume_embeddings, jd_embeddings)

    results = []
    for i, r_skill in enumerate(resume_skills):
        best_match_index = int(np.argmax(similarity_matrix[i]))
        similarity_score = similarity_matrix[i][best_match_index]

        if similarity_score >= threshold_match:
            status = "Matched"
        elif similarity_score >= threshold_weak:
            status = "Weak Match"
        else:
            status = "Missing"

        results.append({
            "Resume Skill": r_skill,
            "Closest JD Skill": jd_skills[best_match_index],
            "Similarity Score": round(float(similarity_score), 2),
            "Status": status
        })

    return results, similarity_matrix.tolist()

# ---- ADD BELOW THIS LINE ----

def compute_similarity(resume_skills, jd_skills):
    """Return overall similarity score as percentage."""
    results, _ = compare_skills(resume_skills, jd_skills)
    if not results:
        return 0.0

    scores = [item["Similarity Score"] for item in results]
    return round((sum(scores) / len(scores)) * 100, 2)

def classify_gap(resume_skills, jd_skills):
    """Return matched and missing skills based on comparison."""
    results, _ = compare_skills(resume_skills, jd_skills)

    matched = [r["Resume Skill"] for r in results if r["Status"] == "Matched"]
    weak = [r["Resume Skill"] for r in results if r["Status"] == "Weak Match"]

    # Missing skills = those in JD but not strong enough in Resume
    missing = list(set(jd_skills) - set(matched) - set(weak))

    return matched, weak, missing
