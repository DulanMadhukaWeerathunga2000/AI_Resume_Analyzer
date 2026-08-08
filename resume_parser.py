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

    text = text.lower()

    sections = {
        "summary": False,
        "skills": False,
        "education": False,
        "experience": False,
        "projects": False,
        "certifications": False
    }

    keywords = {

        "summary": [
            "summary",
            "professional summary",
            "profile",
            "objective"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "education": [
            "education",
            "academic qualifications"
        ],

        "experience": [
            "experience",
            "work experience",
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
        ]
    }

    for section, words in keywords.items():

        for word in words:

            if word in text:

                sections[section] = True
                break

    return sections