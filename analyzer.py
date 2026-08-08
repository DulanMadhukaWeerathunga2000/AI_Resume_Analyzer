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

    "machine learning",
    "data analysis",

    "c",
    "c++",
    "c#",

    "php",
    "laravel",

    "spring boot",

    "rest api",
    "api",

    "bootstrap"
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
    "collaboration"
]


ALL_SKILLS = TECHNICAL_SKILLS + SOFT_SKILLS


def skill_exists(text, skill):

    text = text.lower()

    skill = skill.lower()

    if skill == "node.js":

        return bool(
            re.search(
                r"\bnode\s*\.?\s*js\b",
                text
            )
        )

    escaped_skill = re.escape(skill)

    pattern = (
        r"(?<!\w)"
        + escaped_skill
        + r"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            text
        )
    )


def extract_required_skills(job_description):

    required = []

    for skill in ALL_SKILLS:

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

    required = extract_required_skills(
        job_description
    )

    matched = []
    missing = []

    for skill in required:

        if skill_exists(
            resume_text,
            skill
        ):

            matched.append(skill)

        else:

            missing.append(skill)

    if required:

        score = round(
            len(matched)
            /
            len(required)
            *
            100
        )

    else:

        score = 0

    return (
        score,
        matched,
        missing
    )


def get_skill_scores(
    resume_text,
    job_description
):

    required = extract_required_skills(
        job_description
    )

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


def get_category_scores(
    resume_text,
    job_description
):

    technical_required = []

    soft_required = []

    for skill in TECHNICAL_SKILLS:

        if skill_exists(
            job_description,
            skill
        ):

            technical_required.append(skill)


    for skill in SOFT_SKILLS:

        if skill_exists(
            job_description,
            skill
        ):

            soft_required.append(skill)


    technical_matched = []

    for skill in technical_required:

        if skill_exists(
            resume_text,
            skill
        ):

            technical_matched.append(skill)


    soft_matched = []

    for skill in soft_required:

        if skill_exists(
            resume_text,
            skill
        ):

            soft_matched.append(skill)


    if technical_required:

        technical_score = round(
            len(technical_matched)
            /
            len(technical_required)
            *
            100
        )

    else:

        technical_score = 0


    if soft_required:

        soft_score = round(
            len(soft_matched)
            /
            len(soft_required)
            *
            100
        )

    else:

        soft_score = 0


    return {
        "technical": technical_score,
        "soft": soft_score
    }


def get_score_status(score):

    if score >= 80:

        return (
            "Excellent Match",
            "Your resume strongly matches the job requirements."
        )

    elif score >= 60:

        return (
            "Good Match",
            "Your resume matches many of the required skills."
        )

    elif score >= 40:

        return (
            "Needs Improvement",
            "Your resume has some relevant skills but can be improved."
        )

    else:

        return (
            "Low Match",
            "Your resume needs more job-related skills."
        )


def generate_suggestions(
    score,
    missing_skills,
    sections
):

    suggestions = []


    if score >= 80:

        suggestions.append(
            "Your resume is strongly aligned with this position."
        )

    elif score >= 60:

        suggestions.append(
            "Add relevant missing skills to improve your match."
        )

    elif score >= 40:

        suggestions.append(
            "Customize your resume according to the job description."
        )

    else:

        suggestions.append(
            "Add more relevant technical skills and projects."
        )


    if missing_skills:

        suggestions.append(
            "Consider adding these skills if you have experience with them: "
            + ", ".join(missing_skills)
        )


    if not sections["summary"]:

        suggestions.append(
            "Add a professional summary."
        )


    if not sections["skills"]:

        suggestions.append(
            "Create a dedicated Technical Skills section."
        )


    if not sections["education"]:

        suggestions.append(
            "Add your education qualifications."
        )


    if not sections["experience"]:

        suggestions.append(
            "Add internship, work, or relevant experience."
        )


    if not sections["projects"]:

        suggestions.append(
            "Add 2–3 relevant projects with technologies used."
        )


    if not sections["certifications"]:

        suggestions.append(
            "Add relevant certifications or online courses."
        )


    return suggestions