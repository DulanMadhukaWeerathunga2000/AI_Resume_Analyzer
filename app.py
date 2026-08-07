import os

from flask import Flask, render_template, request

from database import create_database, save_analysis
from resume_parser import extract_text_from_pdf
from analyzer import analyze_resume


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

create_database()


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]

    job_description = request.form["job_description"]

    if resume.filename == "":
        return "Please upload a resume."

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(file_path)

    resume_text = extract_text_from_pdf(file_path)

    score, matched, missing = analyze_resume(
        resume_text,
        job_description
    )

    save_analysis(
        resume.filename,
        score,
        matched,
        missing
    )

    return render_template(
        "result.html",
        score=score,
        matched=matched,
        missing=missing
    )


if __name__ == "__main__":

    app.run(debug=True)