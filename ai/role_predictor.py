def predict_role(resume_text, role_skills_map):
    """
    Predict best matching role based on skill overlap
    """
    best_role = None
    best_score = 0

    resume_text = resume_text.lower()

    for role, skills in role_skills_map.items():
        match_count = 0

        for skill in skills:
            if skill.lower() in resume_text:
                match_count += 1

        if match_count > best_score:
            best_score = match_count
            best_role = role

    return best_role, best_score