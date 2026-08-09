from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pathlib import Path
import os

from resume_parser import extract_text_from_pdf, analyze_resume_sections
from analyzer import analyze_resume
from database import init_db, save_analysis, get_all_analyses, get_analysis

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

init_db()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        flash("Please select a PDF resume.")
        return redirect(url_for("home"))

    resume = request.files["resume"]
    job_description = request.form.get("job_description", "").strip()

    if not resume or resume.filename == "":
        flash("Please select a resume PDF.")
        return redirect(url_for("home"))

    if not allowed_file(resume.filename):
        flash("Only PDF files are supported.")
        return redirect(url_for("home"))

    if not job_description:
        flash("Please enter a job description.")
        return redirect(url_for("home"))

    filename = secure_filename(resume.filename)
    file_path = UPLOAD_FOLDER / filename
    resume.save(file_path)

    try:
        resume_text = extract_text_from_pdf(str(file_path))

        if not resume_text.strip():
            flash("Could not extract text from the PDF. Try a text-based PDF.")
            return redirect(url_for("home"))

        result = analyze_resume(resume_text, job_description)
        result["sections"] = analyze_resume_sections(resume_text)

        analysis_id = save_analysis(
            filename=filename,
            job_description=job_description,
            result=result
        )

        return render_template(
            "result.html",
            result=result,
            analysis_id=analysis_id,
            filename=filename
        )

    except Exception as exc:
        app.logger.exception("Analysis failed")
        flash(f"Analysis failed: {exc}")
        return redirect(url_for("home"))

    finally:
        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass


@app.route("/history")
def history():
    analyses = get_all_analyses()
    return render_template("history.html", analyses=analyses)


@app.route("/history/<int:analysis_id>")
def history_detail(analysis_id):
    analysis = get_analysis(analysis_id)

    if not analysis:
        flash("Analysis not found.")
        return redirect(url_for("history"))

    return render_template(
        "result.html",
        result=analysis["result"],
        analysis_id=analysis["id"],
        filename=analysis["filename"]
    )


if __name__ == "__main__":
    app.run(debug=True)
