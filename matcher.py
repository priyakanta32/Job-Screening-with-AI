import re

def simple_text_extractor(text):
    """Extracts simple keywords from text."""
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return set(words)

def match_cv_to_jd(cv_skills, jd_skills):
    if not cv_skills or not jd_skills:
        return 0.0

    matches = sum(1 for skill in jd_skills if skill.lower() in [s.lower() for s in cv_skills])
    match_score = (matches / len(jd_skills)) * 100
    return round(match_score, 2)

