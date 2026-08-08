import re


SKILLS = [
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

    "machine learning",
    "data analysis",

    "communication",
    "teamwork",
    "problem solving",

    "project management"
]


def skill_exists(text, skill):

    text = text.lower()

    if skill.lower() == "node.js":

        return bool(
            re.search(
                r"\bnode\s*\.?\s*js\b",
                text
            )
        )

    pattern = (
        r"(?<!\w)"
        + re.escape(skill.lower())
        + r"(?!\w)"
    )

    return bool(
        re.search(pattern, text)
    )


def extract_required_skills(job_description):

    required = []

    for skill in SKILLS:

        if skill_exists(
            job_description,
            skill
        ):
            required.append(skill)

    return required


def analyze_skills(
    resume_text,
    job_description
):

    required_skills = extract_required_skills(
        job_description
    )

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill_exists(
            resume_text,
            skill
        ):
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    if required_skills:

        score = round(
            len(matched_skills)
            /
            len(required_skills)
            * 100
        )

    else:

        score = 0

    return (
        score,
        matched_skills,
        missing_skills
    )


def get_score_status(score):

    if score >= 80:

        return (
            "Excellent Match",
            "Your resume strongly matches the job requirements."
        )

    if score >= 60:

        return (
            "Good Match",
            "Your resume matches many of the required skills."
        )

    if score >= 40:

        return (
            "Needs Improvement",
            "Your resume has some relevant skills but can be improved."
        )

    return (
        "Low Match",
        "Consider improving your resume with more relevant skills."
    )


def generate_suggestions(
    score,
    missing_skills,
    sections
):

    suggestions = []

    if score >= 80:

        suggestions.append(
            "Your resume has a strong skill match for this position."
        )

    elif score >= 60:

        suggestions.append(
            "Add more relevant skills to improve your job match."
        )

    elif score >= 40:

        suggestions.append(
            "Add more job-related technical skills and projects."
        )

    else:

        suggestions.append(
            "Review the job description and tailor your resume to the position."
        )

    if missing_skills:

        suggestions.append(
            "Relevant missing skills: "
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
            "Add relevant work experience or internship experience."
        )

    if not sections["projects"]:

        suggestions.append(
            "Add relevant academic or personal projects."
        )

    if not sections["certifications"]:

        suggestions.append(
            "Add relevant certifications or courses."
        )

    return suggestions