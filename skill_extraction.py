# skill_extraction.py

import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def load_skills_list(path="data/skills_list.txt"):
    skills = []
    with open(path, "r") as file:
        for line in file:
            s = line.strip()
            if s:
                skills.append(s.lower())
    return skills

def extract_skills_keyword(text, skills_list):
    text = text.lower()
    found = set()
    for skill in skills_list:
        if skill in text:
            found.add(skill)
    return list(found)

def extract_skills_spacy(text, top_k=40):
    doc = nlp(text)
    candidates = []
    for chunk in doc.noun_chunks:
        txt = chunk.text.strip().lower()
        if 1 < len(txt) <= 30:  # phrase length filter
            candidates.append(txt)
    freq = Counter(candidates)
    return [s for s,_ in freq.most_common(top_k)]

def simple_keyword_skills(text, skills_list):
    return extract_skills_keyword(text, skills_list)

def spacy_candidate_skills(text):
    return extract_skills_spacy(text)


