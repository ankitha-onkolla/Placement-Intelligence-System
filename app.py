
import os
import re
import pymupdf as fitz
from docx import Document
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Upload settings
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def extract_resume_text(filepath):
    extension = filepath.rsplit(".", 1)[1].lower()

    if extension == "pdf":
        text = ""
        with fitz.open(filepath) as pdf:
            for page in pdf:
                text += page.get_text() + "\n"
        return text

    if extension == "docx":
        document = Document(filepath)
        return "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    return ""


def analyze_skills(text):
    skills_list = [
        "Python", "Java", "C", "C++", "SQL",
        "HTML", "CSS", "JavaScript", "React",
        "Flask", "Django", "Machine Learning",
        "Data Science", "Data Analytics",
        "Excel", "Power BI", "MongoDB",
        "MySQL", "Communication", "Git"
    ]

    found_skills = []

    for skill in skills_list:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return "No resume file selected. <a href='/'>Go back</a>"

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume. <a href='/'>Go back</a>"

    if not allowed_file(file.filename):
        return "Only PDF and DOCX files are allowed. <a href='/'>Go back</a>"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    try:
        resume_text = extract_resume_text(filepath)

        if not resume_text.strip():
            return (
                "No readable text found. Please upload a text-based PDF "
                "or DOCX resume. <a href='/'>Go back</a>"
            )

        skills = analyze_skills(resume_text)

        result_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resume Analysis Results</title>
            <style>
                body {
                    font-family: Arial;
                    background: #f1f5fb;
                    padding: 30px;
                    color: #172554;
                }
                .container {
                    background: white;
                    max-width: 700px;
                    margin: auto;
                    padding: 30px;
                    border-radius: 12px;
                }
                .skill {
                    display: inline-block;
                    background: #dbeafe;
                    color: #1d4ed8;
                    padding: 10px 15px;
                    margin: 6px;
                    border-radius: 20px;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    background: #2563eb;
                    color: white;
                    padding: 12px 20px;
                    text-decoration: none;
                    border-radius: 7px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Resume Analysis Results</h1>
                <p><b>File:</b> {{ filename }}</p>
                <h2>Skills Identified</h2>
                {% if skills %}
                    {% for skill in skills %}
                        <span class="skill">{{ skill }}</span>
                    {% endfor %}
                {% else %}
                    <p>No matching skills identified.</p>
                {% endif %}
                <h3>Total Skills Found: {{ skills|length }}</h3>
                <p>
                    This is a basic keyword-based resume analysis,
                    not a validated AI placement prediction.
                </p>
                <a href="/">Back to Dashboard</a>
            </div>
        </body>
        </html>
        """

        from flask import render_template_string

        return render_template_string(
            result_html,
            filename=filename,
            skills=skills
        )

    except Exception as error:
        return (
            "Could not analyze the resume. Check that the file is valid. "
            "<a href='/'>Go back</a>"
        ), 400


@app.route("/health")
def health():
    return {
        "status": "success",
        "message": "Placement Intelligence System is running"
    }


@app.errorhandler(413)
def file_too_large(error):
    return "File is too large. Maximum allowed size is 10 MB.", 413


if __name__ == "__main__":
    app.run(debug=True)
