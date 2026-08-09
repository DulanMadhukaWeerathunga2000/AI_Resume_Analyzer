from PyPDF2 import PdfReader
import re


def extract_text_from_pdf(file_path):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    return text


def clean_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def analyze_resume_sections(text):
    text_lower = text.lower()

    sections = {
        "contact": False,
        "summary": False,
        "skills": False,
        "education": False,
        "experience": False,
        "projects": False,
        "certifications": False,
    }

    keywords = {
        "contact": ["@", "phone", "email", "linkedin", "github"],
        "summary": ["summary", "professional summary", "profile", "objective"],
        "skills": ["skills", "technical skills", "technologies"],
        "education": ["education", "academic qualifications", "qualifications"],
        "experience": ["experience", "work experience", "employment", "internship"],
        "projects": ["projects", "academic projects", "personal projects"],
        "certifications": ["certifications", "certificates", "training", "courses"],
    }

    for section, words in keywords.items():
        if any(word in text_lower for word in words):
            sections[section] = True

    return sections
