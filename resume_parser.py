from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path):

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def detect_sections(text):

    text_lower = text.lower()

    sections = {
        "summary": False,
        "education": False,
        "experience": False,
        "skills": False,
        "projects": False,
        "certifications": False
    }

    keywords = {

        "summary": [
            "summary",
            "profile",
            "objective"
        ],

        "education": [
            "education",
            "academic"
        ],

        "experience": [
            "experience",
            "employment",
            "work experience"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "projects": [
            "projects",
            "academic projects"
        ],

        "certifications": [
            "certification",
            "certifications"
        ]
    }

    for section, words in keywords.items():

        for word in words:

            if word in text_lower:

                sections[section] = True

                break

    return sections