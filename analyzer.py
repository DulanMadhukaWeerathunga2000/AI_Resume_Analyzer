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

    skill = skill.lower()


    # Special handling for Node.js

    if skill == "node.js":

        pattern = r"\bnode\s*\.?\s*js\b"

        return bool(
            re.search(pattern, text)
        )


    # Prevent java matching inside javascript

    pattern = (
        r"(?<!\w)"
        + re.escape(skill)
        + r"(?!\w)"
    )


    return bool(
        re.search(pattern, text)
    )


def extract_required_skills(job_description):

    required_skills = []


    for skill in SKILLS:

        if skill_exists(
            job_description,
            skill
        ):

            required_skills.append(skill)


    return required_skills


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
            (
                len(matched_skills)
                /
                len(required_skills)
            ) * 100
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
            "Your resume has a strong match with the job requirements."
        )


    elif score >= 60:

        return (
            "Good Match",
            "Your resume matches many of the job requirements."
        )


    elif score >= 40:

        return (
            "Needs Improvement",
            "Your resume has some relevant skills but could be improved."
        )


    else:

        return (
            "Low Match",
            "Your resume needs significant improvement for this position."
        )


def generate_suggestions(
    score,
    missing_skills,
    sections
):

    suggestions = []


    # Score suggestion

    if score >= 80:

        suggestions.append(
            "Your resume has a strong match with this job."
        )


    elif score >= 60:

        suggestions.append(
            "Your resume is a good match. Add more relevant skills to improve the score."
        )


    elif score >= 40:

        suggestions.append(
            "Consider adding more job-relevant skills and experience."
        )


    else:

        suggestions.append(
            "Review the job requirements and improve your resume with relevant skills and projects."
        )


    # Missing skills

    if missing_skills:

        suggestions.append(
            "Consider adding these skills if you genuinely have them: "
            + ", ".join(missing_skills)
        )


    # Resume sections

    if not sections.get("summary"):

        suggestions.append(
            "Add a professional summary at the beginning of your resume."
        )


    if not sections.get("skills"):

        suggestions.append(
            "Add a dedicated Technical Skills section."
        )


    if not sections.get("education"):

        suggestions.append(
            "Add an Education section."
        )


    if not sections.get("experience"):

        suggestions.append(
            "Add relevant internship, work, or practical experience."
        )


    if not sections.get("projects"):

        suggestions.append(
            "Add relevant academic or personal projects."
        )


    if not sections.get("certifications"):

        suggestions.append(
            "Add relevant certifications, courses, or training."
        )


    return suggestions