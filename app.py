import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file
)

from database import (
    create_database,
    save_analysis,
    get_all_analyses,
    delete_analysis
)

from resume_parser import (
    extract_text_from_pdf,
    detect_sections
)

from analyzer import (
    analyze_skills,
    get_score_status,
    generate_suggestions
)

from report import generate_report


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER


create_database()


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    resume = request.files.get(
        "resume"
    )

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    if not resume:

        return "Please upload a resume."


    if not resume.filename:

        return "Please select a file."


    if not resume.filename.lower().endswith(
        ".pdf"
    ):

        return "Only PDF files are supported."


    if not job_description:

        return "Please enter a job description."


    filename = resume.filename


    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    resume.save(
        file_path
    )


    try:

        resume_text = extract_text_from_pdf(
            file_path
        )

    except Exception as error:

        return (
            "Error reading PDF: "
            + str(error)
        )


    if not resume_text.strip():

        return (
            "Could not extract text from this PDF."
        )


    score, matched, missing = analyze_skills(
        resume_text,
        job_description
    )


    status, status_message = get_score_status(
        score
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


    report_filename = generate_report(
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

        status=status,

        status_message=status_message,

        matched=matched,

        missing=missing,

        suggestions=suggestions,

        sections=sections,

        report_filename=report_filename
    )


@app.route("/dashboard")
def dashboard():

    analyses = get_all_analyses()


    scores = [
        row["score"]
        for row in analyses
    ]


    total = len(analyses)


    if scores:

        average = round(
            sum(scores) / len(scores)
        )

        highest = max(scores)

        lowest = min(scores)

    else:

        average = 0
        highest = 0
        lowest = 0


    recent = analyses[:5]


    return render_template(
        "dashboard.html",

        total_analyses=total,

        average_score=average,

        highest_score=highest,

        lowest_score=lowest,

        recent_analyses=recent
    )


@app.route("/history")
def history():

    analyses = get_all_analyses()

    return render_template(
        "history.html",
        analyses=analyses
    )


@app.route(
    "/download/<path:filename>"
)
def download(filename):

    file_path = os.path.join(
        REPORT_FOLDER,
        filename
    )


    if not os.path.exists(file_path):

        return "Report not found."


    return send_file(
        file_path,
        as_attachment=True
    )


@app.route(
    "/delete/<int:analysis_id>",
    methods=["POST"]
)
def delete(analysis_id):

    delete_analysis(
        analysis_id
    )

    return redirect(
        url_for("history")
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )