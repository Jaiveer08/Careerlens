def extract_skills(resume_text, role_skills):
    """
    Extract skills present in resume text
    """
    found_skills = []

    for skill in role_skills:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    return found_skills