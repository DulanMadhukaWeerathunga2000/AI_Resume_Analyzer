from PyPDF2 import PdfReader
import re


def extract_text_from_pdf(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def clean_text(text):

    text = text.replace("\x00", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def detect_sections(text):

    text_lower = text.lower()

    sections = {

        "summary": False,
        "skills": False,
        "education": False,
        "experience": False,
        "projects": False,
        "certifications": False,
        "contact": False

    }

    section_keywords = {

        "summary": [
            "summary",
            "professional summary",
            "profile",
            "objective"
        ],

        "skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "education": [
            "education",
            "academic qualifications",
            "qualifications"
        ],

        "experience": [
            "experience",
            "work experience",
            "employment",
            "internship"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "certifications": [
            "certifications",
            "certificates",
            "courses",
            "training"
        ],

        "contact": [
            "@",
            "phone",
            "email",
            "linkedin",
            "github"
        ]

    }

    for section, keywords in section_keywords.items():

        for keyword in keywords:

            if keyword in text_lower:

                sections[section] = True

                break

    return sections