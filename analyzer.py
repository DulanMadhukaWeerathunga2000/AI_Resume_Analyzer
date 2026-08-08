import re
from collections import Counter

import spacy


# Load NLP model
try:

    nlp = spacy.load(
        "en_core_web_sm"
    )

except OSError:

    nlp = None


# --------------------------------------------------
# SKILL DATABASE
# --------------------------------------------------

TECHNICAL_SKILLS = [

    "python",
    "java",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "react.js",
    "node.js",
    "flask",
    "django",

    "sql",
    "mysql",
    "postgresql",
    "sqlite",

    "mongodb",
    "oracle",

    "git",
    "github",
    "gitlab",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "google cloud",

    "machine learning",
    "deep learning",
    "artificial intelligence",

    "data analysis",
    "data science",

    "numpy",
    "pandas",
    "matplotlib",

    "c",
    "c++",
    "c#",
    "php",

    "spring boot",
    "laravel",

    "rest api",
    "api",

    "bootstrap",

    "figma",

    "power bi",
    "excel",
    "tableau",

    "linux",
    "windows",

    "networking",
    "tcp/ip",
    "computer networking",

    "cybersecurity",
    "network security"

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
    "organization",
    "presentation",
    "decision making"

]


ALL_SKILLS = (
    TECHNICAL_SKILLS
    + SOFT_SKILLS
)


# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def normalize_text(text):

    text = text.lower()

    replacements = {

        "node js": "node.js",

        "nodejs": "node.js",

        "react js": "react.js",

        "reactjs": "react.js",

        "restful api": "rest api",

        "restful apis": "rest api",

        "machine-learning":
            "machine learning",

        "deep-learning":
            "deep learning",

        "artificial-intelligence":
            "artificial intelligence"

    }


    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )


    return text


# --------------------------------------------------
# SKILL MATCH
# --------------------------------------------------

def skill_exists(text, skill):

    text = normalize_text(text)

    skill = skill.lower()

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


# --------------------------------------------------
# NLP KEYWORD EXTRACTION
# --------------------------------------------------

def extract_nlp_keywords(text):

    if not nlp:

        return []


    doc = nlp(text)

    keywords = []


    for chunk in doc.noun_chunks:

        phrase = chunk.text.strip().lower()

        phrase = re.sub(
            r"[^a-zA-Z0-9+#./ -]",
            "",
            phrase
        )

        if len(phrase) < 3:

            continue


        if phrase not in keywords:

            keywords.append(
                phrase
            )


    # Add important entities

    for token in doc:

        if token.pos_ in (
            "NOUN",
            "PROPN"
        ):

            word = token.text.lower()

            if len(word) >= 3:

                if word not in keywords:

                    keywords.append(word)


    # Frequency based keywords

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z+#.]{2,}\b",
        text.lower()
    )


    frequency = Counter(words)


    for word, count in frequency.most_common(30):

        if count >= 2:

            if word not in keywords:

                keywords.append(word)


    return keywords[:100]


# --------------------------------------------------
# EXTRACT SKILLS
# --------------------------------------------------

def extract_skills(text):

    found = []

    for skill in ALL_SKILLS:

        if skill_exists(
            text,
            skill
        ):

            found.append(skill)


    return found


# --------------------------------------------------
# JOB REQUIREMENTS
# --------------------------------------------------

def extract_required_skills(
    job_description
):

    return extract_skills(
        job_description
    )


# --------------------------------------------------
# SKILL ANALYSIS
# --------------------------------------------------

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

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )


    if required:

        score = round(
            len(matched)
            /
            len(required)
            * 100
        )

    else:

        score = 0


    return (
        score,
        matched,
        missing
    )


# --------------------------------------------------
# CATEGORY SCORES
# --------------------------------------------------

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

            technical_required.append(
                skill
            )


    for skill in SOFT_SKILLS:

        if skill_exists(
            job_description,
            skill
        ):

            soft_required.append(
                skill
            )


    technical_matched = [

        skill

        for skill in technical_required

        if skill_exists(
            resume_text,
            skill
        )

    ]


    soft_matched = [

        skill

        for skill in soft_required

        if skill_exists(
            resume_text,
            skill
        )

    ]


    if technical_required:

        technical_score = round(

            len(technical_matched)
            /
            len(technical_required)
            * 100

        )

    else:

        technical_score = 0


    if soft_required:

        soft_score = round(

            len(soft_matched)
            /
            len(soft_required)
            * 100

        )

    else:

        soft_score = 0


    return {

        "technical":
            technical_score,

        "soft":
            soft_score

    }


# --------------------------------------------------
# KEYWORD ANALYSIS
# --------------------------------------------------

def keyword_analysis(
    resume_text,
    job_description
):

    resume_keywords = set(
        extract_nlp_keywords(
            resume_text
        )
    )


    job_keywords = set(
        extract_nlp_keywords(
            job_description
        )
    )


    common_keywords = (

        resume_keywords
        &
        job_keywords

    )


    missing_keywords = (

        job_keywords
        -
        resume_keywords

    )


    return {

        "resume_keywords":
            sorted(
                resume_keywords
            )[:50],

        "job_keywords":
            sorted(
                job_keywords
            )[:50],

        "common_keywords":
            sorted(
                common_keywords
            )[:50],

        "missing_keywords":
            sorted(
                missing_keywords
            )[:50]

    }


# --------------------------------------------------
# SECTION SCORE
# --------------------------------------------------

def calculate_section_score(
    sections
):

    if not sections:

        return 0


    found = sum(
        1
        for value
        in sections.values()
        if value
    )


    return round(
        found
        /
        len(sections)
        * 100
    )


# --------------------------------------------------
# ATS SCORE
# --------------------------------------------------

def calculate_ats_score(

    resume_text,

    job_description,

    sections

):

    skill_score, matched, missing = (
        analyze_skills(
            resume_text,
            job_description
        )
    )


    section_score = calculate_section_score(
        sections
    )


    keyword_data = keyword_analysis(

        resume_text,

        job_description

    )


    job_keywords = keyword_data[
        "job_keywords"
    ]


    common_keywords = keyword_data[
        "common_keywords"
    ]


    if job_keywords:

        nlp_keyword_score = round(

            len(common_keywords)
            /
            len(job_keywords)
            * 100

        )

    else:

        nlp_keyword_score = 0


    ats_score = round(

        (
            skill_score * 0.50
        )
        +
        (
            nlp_keyword_score * 0.25
        )
        +
        (
            section_score * 0.25
        )

    )


    return min(
        ats_score,
        100
    )


# --------------------------------------------------
# SKILL DETAILS
# --------------------------------------------------

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

            "skill":
                skill,

            "score":
                100 if found else 0,

            "matched":
                found

        })


    return results


# --------------------------------------------------
# STATUS
# --------------------------------------------------

def get_score_status(
    score
):

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


# --------------------------------------------------
# SUGGESTIONS
# --------------------------------------------------

def generate_suggestions(

    score,

    missing_skills,

    sections,

    missing_keywords=None

):

    suggestions = []


    if score >= 80:

        suggestions.append(

            "Your resume has a strong match with the job description."

        )


    elif score >= 60:

        suggestions.append(

            "Your resume is a good match. Add the remaining relevant keywords."

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

            "Important missing skills: "
            +
            ", ".join(
                missing_skills[:15]
            )

        )


    if missing_keywords:

        suggestions.append(

            "Consider reviewing these job-description keywords: "
            +
            ", ".join(
                missing_keywords[:10]
            )

        )


    if not sections.get(
        "summary",
        False
    ):

        suggestions.append(

            "Add a professional summary."

        )


    if not sections.get(
        "skills",
        False
    ):

        suggestions.append(

            "Add a dedicated Technical Skills section."

        )


    if not sections.get(
        "education",
        False
    ):

        suggestions.append(

            "Add your education qualifications."

        )


    if not sections.get(
        "experience",
        False
    ):

        suggestions.append(

            "Add internship or relevant experience."

        )


    if not sections.get(
        "projects",
        False
    ):

        suggestions.append(

            "Add 2–3 relevant projects with technologies used."

        )


    if not sections.get(
        "certifications",
        False
    ):

        suggestions.append(

            "Add relevant certifications or courses."

        )


    return suggestions


# --------------------------------------------------
# COMPLETE ANALYSIS
# --------------------------------------------------

def analyze_resume(

    resume_text,

    job_description,

    sections

):

    match_score, matched, missing = (
        analyze_skills(

            resume_text,

            job_description

        )
    )


    ats_score = calculate_ats_score(

        resume_text,

        job_description,

        sections

    )


    category_scores = get_category_scores(

        resume_text,

        job_description

    )


    keyword_data = keyword_analysis(

        resume_text,

        job_description

    )


    suggestions = generate_suggestions(

        match_score,

        missing,

        sections,

        keyword_data[
            "missing_keywords"
        ]

    )


    status, status_message = (
        get_score_status(
            match_score
        )
    )


    skill_scores = get_skill_scores(

        resume_text,

        job_description

    )


    return {

        "match_score":
            match_score,

        "ats_score":
            ats_score,

        "matched":
            matched,

        "missing":
            missing,

        "status":
            status,

        "status_message":
            status_message,

        "suggestions":
            suggestions,

        "skill_scores":
            skill_scores,

        "category_scores":
            category_scores,

        "keyword_data":
            keyword_data

    }