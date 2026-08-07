import os

from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from database import (
    create_database,
    save_analysis,
    get_all_analyses
)

from resume_parser import (
    extract_text_from_pdf,
    detect_sections
)

from analyzer import (
    analyze_skills,
    generate_suggestions
)

from report import generate_report


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

create_database()


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")

    job_description = request.form.get(
        "job_description",
        ""
    )


    if not resume:

        return "Please upload a resume."


    if not resume.filename.lower().endswith(".pdf"):

        return "Only PDF files are allowed."


    filename = resume.filename

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    resume.save(file_path)


    resume_text = extract_text_from_pdf(
        file_path
    )


    if not resume_text.strip():

        return "Could not extract text from the PDF."


    score, matched, missing = analyze_skills(
        resume_text,
        job_description
    )


    sections = detect_sections(
        resume_text
    )


    suggestions = generate_suggestions(
        score,
        missing,
        sections
    )


    save_analysis(
        filename,
        score,
        matched,
        missing,
        suggestions
    )


    report_file = generate_report(
        filename,
        score,
        matched,
        missing,
        suggestions
    )


    return render_template(
        "result.html",

        filename=filename,

        score=score,

        matched=matched,

        missing=missing,

        suggestions=suggestions,

        sections=sections
    )


@app.route("/history")
def history():

    analyses = get_all_analyses()

    return render_template(
        "history.html",
        analyses=analyses
    )


@app.route("/download/<filename>")
def download(filename):

    path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    if os.path.exists(path):

        return send_file(
            path,
            as_attachment=True
        )

    return "Report not found."


if __name__ == "__main__":

    app.run(debug=True)