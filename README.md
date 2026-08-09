# 🤖 AI Resume Analyzer

A Python Flask-based web application that analyzes a resume against a job description and provides ATS compatibility, job-match scoring, keyword analysis, skill alignment, and resume improvement suggestions.

## 🚀 Features

* 📄 PDF Resume Upload
* 📝 Job Description Analysis
* 🎯 Job Match Score
* 📊 ATS Compatibility Score
* 💻 Technical Skills Analysis
* 🤝 Soft Skills Analysis
* 🧠 Keyword Matching
* ❌ Missing Keyword Detection
* 🚀 Recommended Skills
* 💪 Resume Strength Analysis
* 💡 Resume Improvement Suggestions
* 📋 Resume Section Analysis
* 🗃️ Analysis History
* 💾 SQLite Database
* 📱 Responsive Web Interface

## 🛠️ Technologies

* Python
* Flask
* PyPDF2
* SQLite
* HTML5
* CSS3
* Jinja2
* Gunicorn

## 📂 Project Structure

```text
AI_Resume_Analyzer/
│
├── app.py
├── analyzer.py
├── database.py
├── resume_parser.py
├── requirements.txt
├── .gitignore
├── .python-version
├── README.md
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── result.html
│   └── history.html
│
└── static/
    └── style.css
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/DulanMadhukaWeerathunga2000/AI_Resume_Analyzer.git
```

### 2. Open the project

```bash
cd AI_Resume_Analyzer
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🔍 How It Works

1. Upload a PDF resume.
2. Paste the target job description.
3. The system extracts text from the resume.
4. The analyzer identifies relevant keywords and skills.
5. Resume and job-description keywords are compared.
6. The system calculates job-match and ATS scores.
7. Missing keywords and recommended skills are displayed.
8. Improvement suggestions are generated.
9. The analysis can be viewed from the history page.

## 📊 Analysis Modules

### Job Match Score

Measures the overlap between keywords found in the resume and the target job description.

### ATS Score

Evaluates resume structure, contact information, skills, and relevant sections.

### Technical Skills

Checks technical skills relevant to the target job.

### Soft Skills

Checks common professional and interpersonal skills.

### Keyword Analysis

Shows:

* Matched keywords
* Missing keywords
* Recommended skills

### Resume Sections

The application checks for sections such as:

* Professional Summary
* Skills
* Education
* Experience
* Projects
* Certifications

## 🌐 Deployment

This application can be deployed as a Python Flask Web Service using Render.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

## 🔄 Continuous Deployment

The project can be connected to GitHub and Render so that new commits pushed to the selected branch can automatically trigger a new deployment.

## ⚠️ Important

This project is intended for educational and portfolio purposes.

The analysis provides recommendations based on keyword and rule-based matching. Scores should be treated as guidance rather than a guarantee of actual ATS results.

## 👨‍💻 Author

**D.M. Weerathunga**

GitHub:

https://github.com/DulanMadhukaWeerathunga2000

## 📄 License

This project is available for educational and portfolio use.
