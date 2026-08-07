SKILLS = [
    "python",
    "java",
    "javascript",
    "react",
    "html",
    "css",
    "sql",
    "mysql",
    "sqlite",
    "flask",
    "django",
    "git",
    "github",
    "docker",
    "linux",
    "aws",
    "communication",
    "teamwork",
    "problem solving"
]


def analyze_resume(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    required_skills = []

    for skill in SKILLS:

        if skill in job_description:
            required_skills.append(skill)

    matched = []
    missing = []

    for skill in required_skills:

        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(required_skills) > 0:
        score = int(
            (len(matched) / len(required_skills)) * 100
        )
    else:
        score = 0

    return score, matched, missing