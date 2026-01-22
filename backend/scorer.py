def calculate_score(found_skills, role_skills):
    """
    Calculate resume score and missing skills
    """
    total_skills = len(role_skills)
    matched_skills = len(found_skills)

    score = int((matched_skills / total_skills) * 100)
    missing_skills = list(set(role_skills) - set(found_skills))

    return score, missing_skills