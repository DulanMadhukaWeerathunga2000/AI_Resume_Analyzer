import os

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for
)


from database import (
    create_database,
    save_analysis,
    get_all_analyses,
    get_analysis,
    delete_analysis
)


from resume_parser import (
    extract_text_from_pdf,
    detect_sections
)


from analyzer import (
    analyze_skills,
    generate_suggestions,
    get_score_status
)


from report import (
    generate_report
)


app = Flask(__name__)


# =====================================
# FOLDERS
# =====================================

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


# =====================================
# DATABASE
# =====================================

create_database()


# =====================================
# HOME
# =====================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================
# ANALYZE RESUME
# =====================================

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
    )


    # Validate resume

    if not resume:

        return "Please upload a resume."


    if not resume.filename:

        return "Please select a resume file."


    if not resume.filename.lower().endswith(
        ".pdf"
    ):

        return "Only PDF files are allowed."


    # Validate job description

    if not job_description.strip():

        return "Please enter a job description."


    # Save uploaded resume

    filename = resume.filename


    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )


    resume.save(
        file_path
    )


    # Extract PDF text

    resume_text = extract_text_from_pdf(
        file_path
    )


    if not resume_text.strip():

        return (
            "Could not extract text from the PDF. "
            "Please upload a text-based PDF."
        )


    # Analyze skills

    (
        score,
        matched,
        missing
    ) = analyze_skills(
        resume_text,
        job_description
    )


    # Score status

    (
        status,
        status_message
    ) = get_score_status(
        score
    )


    # Detect sections

    sections = detect_sections(
        resume_text
    )


    # Suggestions

    suggestions = generate_suggestions(
        score,
        missing,
        sections
    )


    # Save database

    save_analysis(
        filename,
        score,
        matched,
        missing,
        suggestions
    )


    # Generate PDF report

    report_filename = generate_report(
        filename,
        score,
        matched,
        missing,
        suggestions
    )


    # Result page

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


# =====================================
# DASHBOARD
# =====================================

@app.route("/dashboard")
def dashboard():

    analyses = get_all_analyses()


    total_analyses = len(
        analyses
    )


    scores = []


    for analysis in analyses:

        try:

            score = int(
                analysis[2]
            )

            scores.append(
                score
            )

        except (
            ValueError,
            TypeError,
            IndexError
        ):

            pass


    if scores:

        average_score = round(
            sum(scores)
            /
            len(scores)
        )

        highest_score = max(
            scores
        )

        lowest_score = min(
            scores
        )

    else:

        average_score = 0

        highest_score = 0

        lowest_score = 0


    recent_analyses = list(
        reversed(
            analyses[-5:]
        )
    )


    return render_template(
        "dashboard.html",

        total_analyses=total_analyses,

        average_score=average_score,

        highest_score=highest_score,

        lowest_score=lowest_score,

        recent_analyses=recent_analyses
    )


# =====================================
# HISTORY
# =====================================

@app.route("/history")
def history():

    analyses = list(
        reversed(
            get_all_analyses()
        )
    )


    return render_template(
        "history.html",
        analyses=analyses
    )


# =====================================
# DOWNLOAD REPORT
# =====================================

@app.route(
    "/download/<filename>"
)
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


# =====================================
# DELETE ANALYSIS
# =====================================

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


# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )