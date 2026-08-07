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


def extract_required_skills(job_description):

    job_description = job_description.lower()

    required = []

    for skill in SKILLS:

        if skill.lower() in job_description:

            required.append(skill)

    return required


def analyze_skills(resume_text, job_description):

    resume_text = resume_text.lower()

    required = extract_required_skills(
        job_description
    )

    matched = []
    missing = []

    for skill in required:

        if skill.lower() in resume_text:

            matched.append(skill)

        else:

            missing.append(skill)

    if required:

        score = int(
            len(matched) /
            len(required) *
            100
        )

    else:

        score = 0

    return score, matched, missing


def generate_suggestions(
    score,
    missing,
    sections
):

    suggestions = []

    if score < 50:

        suggestions.append(
            "Improve your resume by adding relevant job-specific skills."
        )

    elif score < 75:

        suggestions.append(
            "Your resume has a moderate skill match. Add more relevant skills."
        )

    else:

        suggestions.append(
            "Your resume has a strong skill match."
        )


    if missing:

        suggestions.append(
            "Consider adding these skills if you genuinely have them: "
            + ", ".join(missing)
        )


    if not sections["summary"]:

        suggestions.append(
            "Add a professional summary or career objective."
        )


    if not sections["skills"]:

        suggestions.append(
            "Add a dedicated Technical Skills section."
        )


    if not sections["education"]:

        suggestions.append(
            "Add an Education section."
        )


    if not sections["projects"]:

        suggestions.append(
            "Add relevant academic or personal projects."
        )


    if not sections["certifications"]:

        suggestions.append(
            "Consider adding relevant certifications or courses."
        )


    return suggestions