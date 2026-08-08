import re

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path):

    text = ""


    try:

        reader = PdfReader(file_path)


        for page in reader.pages:

            page_text = page.extract_text()


            if page_text:

                text += page_text + "\n"


    except Exception as error:

        print(
            "PDF extraction error:",
            error
        )


    return text


def detect_sections(text):

    lower_text = text.lower()


    sections = {

        "summary": False,

        "skills": False,

        "education": False,

        "experience": False,

        "projects": False,

        "certifications": False

    }


    summary_keywords = [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective"
    ]


    skills_keywords = [
        "skills",
        "technical skills",
        "technical skills & tools"
    ]


    education_keywords = [
        "education",
        "academic",
        "qualifications"
    ]


    experience_keywords = [
        "experience",
        "work experience",
        "employment",
        "internship"
    ]


    project_keywords = [
        "projects",
        "academic projects",
        "personal projects"
    ]


    certification_keywords = [
        "certifications",
        "certificates",
        "courses",
        "training"
    ]


    for keyword in summary_keywords:

        if keyword in lower_text:

            sections["summary"] = True

            break


    for keyword in skills_keywords:

        if keyword in lower_text:

            sections["skills"] = True

            break


    for keyword in education_keywords:

        if keyword in lower_text:

            sections["education"] = True

            break


    for keyword in experience_keywords:

        if keyword in lower_text:

            sections["experience"] = True

            break


    for keyword in project_keywords:

        if keyword in lower_text:

            sections["projects"] = True

            break


    for keyword in certification_keywords:

        if keyword in lower_text:

            sections["certifications"] = True

            break


    return sections