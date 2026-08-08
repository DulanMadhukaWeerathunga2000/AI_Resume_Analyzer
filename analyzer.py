import re


TECHNICAL_SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node.js",
    "flask",
    "django",
    "sql",
    "mysql",
    "sqlite",
    "mongodb",
    "git",
    "github",
    "docker",
    "linux",
    "aws",
    "azure",
    "machine learning",
    "data analysis",
    "data science",
    "c",
    "c++",
    "c#",
    "php",
    "laravel",
    "spring boot",
    "rest api",
    "api",
    "bootstrap",
    "figma",
    "power bi",
    "excel",
    "tableau"
]


SOFT_SKILLS = [
    "communication",
    "teamwork",
    "problem solving",
    "leadership",
    "time management",
    "critical thinking",
    "adaptability",
    "creativity",
    "collaboration",
    "analytical",
    "organization"
]


ALL_SKILLS = TECHNICAL_SKILLS + SOFT_SKILLS


def normalize_text(text):
    text = text.lower()

    text = text.replace("node js", "node.js")
    text = text.replace("nodejs", "node.js")
    text = text.replace("restful api", "rest api")

    return text


def skill_exists(text, skill):

    text = normalize_text(text)

    skill = skill.lower()

    escaped = re.escape(skill)

    pattern = r"(?<!\w)" + escaped + r"(?!\w)"

    return bool(re.search(pattern, text))


def extract_required_skills(job_description):

    required = []

    for skill in ALL_SKILLS:

        if skill_exists(job_description, skill):
            required.append(skill)

    return required


def analyze_skills(resume_text, job_description):

    required = extract_required_skills(job_description)

    matched = []
    missing = []

    for skill in required:

        if skill_exists(resume_text, skill):
            matched.append(skill)

        else:
            missing.append(skill)

    if required:
        score = round(
            len(matched) / len(required) * 100
        )
    else:
        score = 0

    return score, matched, missing


def get_skill_scores(resume_text, job_description):

    required = extract_required_skills(job_description)

    results = []

    for skill in required:

        found = skill_exists(
            resume_text,
            skill
        )

        results.append({
            "skill": skill,
            "score": 100 if found else 0,
            "matched": found
        })

    return results


def get_category_scores(resume_text, job_description):

    technical_required = []

    soft_required = []

    for skill in TECHNICAL_SKILLS:

        if skill_exists(job_description, skill):
            technical_required.append(skill)

    for skill in SOFT_SKILLS:

        if skill_exists(job_description, skill):
            soft_required.append(skill)

    technical_matched = [
        skill
        for skill in technical_required
        if skill_exists(resume_text, skill)
    ]

    soft_matched = [
        skill
        for skill in soft_required
        if skill_exists(resume_text, skill)
    ]

    if technical_required:

        technical_score = round(
            len(technical_matched)
            / len(technical_required)
            * 100
        )

    else:
        technical_score = 0

    if soft_required:

        soft_score = round(
            len(soft_matched)
            / len(soft_required)
            * 100
        )

    else:
        soft_score = 0

    return {
        "technical": technical_score,
        "soft": soft_score
    }


def calculate_ats_score(
    resume_text,
    job_description,
    sections
):

    skill_score, matched, missing = analyze_skills(
        resume_text,
        job_description
    )

    section_score = 0

    total_sections = len(sections)

    if total_sections > 0:

        found_sections = sum(
            1
            for value in sections.values()
            if value
        )

        section_score = round(
            found_sections
            / total_sections
            * 100
        )

    keyword_score = skill_score

    ats_score = round(
        (keyword_score * 0.70)
        +
        (section_score * 0.30)
    )

    return ats_score


def get_score_status(score):

    if score >= 80:

        return (
            "Excellent Match",
            "Your resume strongly matches this job."
        )

    elif score >= 60:

        return (
            "Good Match",
            "Your resume matches many job requirements."
        )

    elif score >= 40:

        return (
            "Needs Improvement",
            "Your resume has relevant content but can be improved."
        )

    else:

        return (
            "Low Match",
            "Your resume needs significant improvement for this job."
        )


def generate_suggestions(
    score,
    missing_skills,
    sections
):

    suggestions = []

    if score >= 80:

        suggestions.append(
            "Your resume has a strong match with the job description."
        )

    elif score >= 60:

        suggestions.append(
            "Add relevant missing skills to increase your job match."
        )

    elif score >= 40:

        suggestions.append(
            "Customize your resume according to the job description."
        )

    else:

        suggestions.append(
            "Add more relevant skills, projects and experience."
        )

    if missing_skills:

        suggestions.append(
            "Relevant missing keywords: "
            + ", ".join(missing_skills)
        )

    if not sections["summary"]:

        suggestions.append(
            "Add a professional summary."
        )

    if not sections["skills"]:

        suggestions.append(
            "Add a dedicated Technical Skills section."
        )

    if not sections["education"]:

        suggestions.append(
            "Add your education qualifications."
        )

    if not sections["experience"]:

        suggestions.append(
            "Add internship or relevant experience."
        )

    if not sections["projects"]:

        suggestions.append(
            "Add 2–3 relevant projects with technologies used."
        )

    if not sections["certifications"]:

        suggestions.append(
            "Add relevant certifications or courses."
        )

    return suggestions