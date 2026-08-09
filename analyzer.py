import re
from collections import Counter


STOP_WORDS = {
    "the", "and", "for", "with", "that", "this", "from", "are", "you",
    "your", "our", "their", "will", "have", "has", "had", "was", "were",
    "can", "may", "not", "all", "any", "job", "role", "work", "working",
    "using", "use", "used", "into", "about", "who", "what", "when",
    "where", "how", "to", "of", "in", "on", "at", "a", "an", "as",
    "be", "is", "it", "or", "by", "we", "they", "he", "she", "i",
    "their", "our", "must", "should", "such", "other", "more", "than",
    "also", "including", "related", "field", "experience"
}


TECHNICAL_SKILLS = {
    "python", "java", "javascript", "typescript", "c", "c++", "c#",
    "html", "css", "react", "angular", "vue", "node.js", "node",
    "flask", "django", "spring", "spring boot", "sql", "mysql",
    "postgresql", "mongodb", "sqlite", "git", "github", "docker",
    "aws", "azure", "linux", "windows", "rest", "api", "rest api",
    "machine learning", "data analysis", "pandas", "numpy",
    "tensorflow", "pytorch", "cloud", "cloud computing", "kubernetes",
    "ci/cd", "jenkins", "oracle", "firebase", "bootstrap"
}


SOFT_SKILLS = {
    "communication", "communication skills", "teamwork", "leadership",
    "problem solving", "problem-solving", "analytical", "adaptability",
    "time management", "collaboration", "creativity", "critical thinking",
    "decision making", "decision-making", "team player", "organization",
    "attention to detail"
}


def normalize(text):
    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")
    return text


def extract_keywords(text):
    text = normalize(text)

    phrases = set()

    # Known technical and soft skills are kept as phrases.
    all_known = TECHNICAL_SKILLS | SOFT_SKILLS

    for skill in all_known:
        if skill in text:
            phrases.add(skill)

    # Also extract useful single words from the job description.
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#./-]{2,}", text)

    counter = Counter(
        word.lower()
        for word in words
        if word.lower() not in STOP_WORDS
    )

    for word, count in counter.most_common(80):
        if count >= 1:
            phrases.add(word)

    return phrases


def contains_keyword(text, keyword):
    text = normalize(text)
    keyword = normalize(keyword)

    if re.search(r"[^a-z0-9]", keyword):
        return keyword in text

    return re.search(r"\b" + re.escape(keyword) + r"\b", text) is not None


def score_from_ratio(ratio):
    return max(0, min(100, round(ratio * 100)))


def analyze_resume(resume_text, job_description):
    resume = normalize(resume_text)
    job = normalize(job_description)

    job_keywords = extract_keywords(job)

    # Remove generic one-word noise.
    job_keywords = {
        item for item in job_keywords
        if item not in STOP_WORDS and len(item) >= 3
    }

    matched = sorted(
        keyword for keyword in job_keywords
        if contains_keyword(resume, keyword)
    )

    missing = sorted(
        keyword for keyword in job_keywords
        if not contains_keyword(resume, keyword)
    )

    keyword_ratio = (
        len(matched) / len(job_keywords)
        if job_keywords else 0
    )

    match_score = score_from_ratio(keyword_ratio)

    technical_job = {
        skill for skill in TECHNICAL_SKILLS
        if contains_keyword(job, skill)
    }

    soft_job = {
        skill for skill in SOFT_SKILLS
        if contains_keyword(job, skill)
    }

    technical_matched = [
        skill for skill in technical_job
        if contains_keyword(resume, skill)
    ]

    soft_matched = [
        skill for skill in soft_job
        if contains_keyword(resume, skill)
    ]

    technical_score = (
        score_from_ratio(
            len(technical_matched) / len(technical_job)
        )
        if technical_job else 100
    )

    soft_score = (
        score_from_ratio(
            len(soft_matched) / len(soft_job)
        )
        if soft_job else 100
    )

    sections = {
        "summary": bool(re.search(
            r"\b(summary|profile|objective)\b", resume
        )),
        "skills": bool(re.search(
            r"\b(skills|technical skills|technologies)\b", resume
        )),
        "education": bool(re.search(
            r"\b(education|qualifications)\b", resume
        )),
        "experience": bool(re.search(
            r"\b(experience|employment|internship)\b", resume
        )),
        "projects": bool(re.search(
            r"\b(projects|academic projects|personal projects)\b", resume
        )),
        "certifications": bool(re.search(
            r"\b(certifications|certificates|training)\b", resume
        )),
    }

    section_score = score_from_ratio(
        sum(sections.values()) / len(sections)
    )

    # Basic ATS structure score.
    contact_score = 100 if (
        "@" in resume or
        "linkedin" in resume or
        "github" in resume
    ) else 0

    ats_score = round(
        technical_score * 0.35 +
        soft_score * 0.15 +
        section_score * 0.30 +
        contact_score * 0.20
    )

    strengths = []

    if matched:
        strengths.append(
            f"{len(matched)} job-related keywords were found in the resume."
        )

    if technical_score >= 70:
        strengths.append("Good technical-skill alignment with the job description.")

    if soft_score >= 70:
        strengths.append("Good soft-skill alignment.")

    if sections["projects"]:
        strengths.append("Projects section detected.")

    if sections["experience"]:
        strengths.append("Experience section detected.")

    if not strengths:
        strengths.append("The resume contains information that can be improved for this job.")

    suggestions = []

    if technical_score < 70:
        suggestions.append(
            "Add relevant technical skills from the job description if you genuinely have them."
        )

    if soft_score < 70:
        suggestions.append(
            "Add relevant soft skills and demonstrate them with short examples."
        )

    if not sections["summary"]:
        suggestions.append(
            "Add a concise professional summary tailored to the target role."
        )

    if not sections["projects"]:
        suggestions.append(
            "Add 2–4 relevant projects with technologies and measurable outcomes."
        )

    if not sections["experience"]:
        suggestions.append(
            "Add internship, academic, freelance, or relevant practical experience."
        )

    if not sections["certifications"]:
        suggestions.append(
            "Consider adding relevant certifications or completed training."
        )

    if missing:
        suggestions.append(
            "Review the missing keywords and add only those that accurately describe your skills."
        )

    recommended_skills = sorted(
        (technical_job | soft_job) - set(matched)
    )

    return {
        "match_score": match_score,
        "ats_score": ats_score,
        "technical_score": technical_score,
        "soft_score": soft_score,
        "matched_keywords": matched[:40],
        "missing_keywords": missing[:60],
        "strengths": strengths,
        "suggestions": suggestions,
        "recommended_skills": recommended_skills[:30],
        "sections": sections,
    }
