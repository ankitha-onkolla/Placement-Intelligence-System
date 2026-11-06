
import os
import re

import pymupdf as fitz
from docx import Document
from flask import Flask, render_template, request, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SKILLS_LIST = [
    "Python", "Java", "C", "C++", "SQL",
    "HTML", "CSS", "JavaScript", "React",
    "Flask", "Django", "Machine Learning",
    "Data Science", "Data Analytics",
    "Excel", "Power BI", "MongoDB",
    "MySQL", "Communication", "Git"
]

JOB_SKILLS = {
    "Python Developer": [
        "Python", "SQL", "Flask", "Django", "Git"
    ],
    "Data Analyst": [
        "Python", "SQL", "Excel", "Power BI", "Data Analytics"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Git"
    ],
    "Data Scientist": [
        "Python", "SQL", "Machine Learning",
        "Data Science", "Data Analytics"
    ]
}


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
    found_skills = []

    for skill in SKILLS_LIST:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def analyze_skill_gap(found_skills, job_role):
    required_skills = JOB_SKILLS.get(job_role, [])

    available_skills = [
        skill for skill in required_skills
        if skill in found_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    if required_skills:
        match_percentage = round(
            len(available_skills) / len(required_skills) * 100
        )
    else:
        match_percentage = 0

    return available_skills, missing_skills, match_percentage


def recommend_jobs(found_skills):
    recommendations = []

    for role, required_skills in JOB_SKILLS.items():
        matched_skills = [
            skill for skill in required_skills
            if skill in found_skills
        ]

        if required_skills:
            match_percentage = round(
                len(matched_skills) / len(required_skills) * 100
            )
        else:
            match_percentage = 0

        recommendations.append({
            "role": role,
            "match": match_percentage,
            "matched_skills": matched_skills
        })

    recommendations.sort(
        key=lambda item: item["match"],
        reverse=True
    )

    return recommendations


# NEW FEATURE: Placement Readiness Prediction
def predict_placement_readiness(match_percentage):
    score = max(0, min(100, match_percentage))

    if score >= 80:
        status = "High Readiness"
        message = "Your skill profile strongly matches this job role."

    elif score >= 50:
        status = "Moderate Readiness"
        message = "Improve your missing skills to become more job-ready."

    else:
        status = "Needs Improvement"
        message = "Focus on learning the required technical skills."

    return {
        "score": score,
        "status": status,
        "message": message
    }


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return "No resume file selected. <a href='/'>Go back</a>"

    file = request.files["resume"]
    job_role = request.form.get("job_role", "").strip()

    if file.filename == "":
        return "Please select a resume. <a href='/'>Go back</a>"

    if not allowed_file(file.filename):
        return "Only PDF and DOCX files are allowed. <a href='/'>Go back</a>"

    if job_role not in JOB_SKILLS:
        return "Please select a valid job role. <a href='/'>Go back</a>"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    try:
        resume_text = extract_resume_text(filepath)

        if not resume_text.strip():
            return (
                "No readable text found. Upload a text-based PDF or DOCX. "
                "<a href='/'>Go back</a>"
            )

        found_skills = analyze_skills(resume_text)

        available, missing, percentage = analyze_skill_gap(
            found_skills, job_role
        )

        recommendations = recommend_jobs(found_skills)

        readiness = predict_placement_readiness(percentage)

        result_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Placement Analysis Report</title>

            <style>
                * { box-sizing: border-box; }

                body {
                    font-family: Arial, sans-serif;
                    background: #f2f5fc;
                    color: #26334d;
                    padding: 25px;
                }

                .container {
                    max-width: 900px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 3px 12px #0000000d;
                }

                h1, h2 { color: #173c70; }

                h2 { margin-top: 30px; }

                .percentage {
                    font-size: 40px;
                    color: #2463ad;
                    font-weight: bold;
                    margin: 15px 0;
                }

                .skill {
                    display: inline-block;
                    background: #e7f1ff;
                    color: #173c70;
                    padding: 9px 13px;
                    margin: 5px;
                    border-radius: 6px;
                }

                .missing {
                    background: #fff0e9;
                    color: #a23c18;
                }

                .job-card {
                    background: #f6f9ff;
                    border-left: 4px solid #2463ad;
                    padding: 17px;
                    margin: 12px 0;
                    border-radius: 8px;
                }

                .match {
                    color: #167443;
                    font-weight: bold;
                    font-size: 20px;
                }

                .readiness-card {
                    background: #edf6ff;
                    border-left: 5px solid #2463ad;
                    padding: 20px;
                    margin-top: 20px;
                    border-radius: 8px;
                }

                .readiness-score {
                    font-size: 42px;
                    font-weight: bold;
                    color: #2463ad;
                    margin: 10px 0;
                }

                .progress {
                    width: 100%;
                    height: 14px;
                    background: #dce5f2;
                    border-radius: 10px;
                    overflow: hidden;
                }

                .progress-fill {
                    height: 100%;
                    background: #2463ad;
                    width: {{ readiness.score }}%;
                }

                .note {
                    background: #fff8df;
                    padding: 15px;
                    border-radius: 7px;
                    line-height: 1.6;
                    margin-top: 25px;
                }

                a {
                    display: inline-block;
                    margin-top: 25px;
                    background: #2463ad;
                    color: white;
                    padding: 12px 20px;
                    text-decoration: none;
                    border-radius: 7px;
                }

                @media(max-width: 600px) {
                    .container { padding: 18px; }
                }
            </style>
        </head>

        <body>
            <div class="container">

                <h1>Placement Intelligence Report</h1>

                <p><b>Resume:</b> {{ filename }}</p>
                <p><b>Selected Job Role:</b> {{ job_role }}</p>

                <h2>Job Skill Match</h2>
                <div class="percentage">{{ percentage }}%</div>

                <h2>Placement Readiness Prediction</h2>

                <div class="readiness-card">
                    <h3>{{ readiness.status }}</h3>

                    <div class="readiness-score">
                        {{ readiness.score }}%
                    </div>

                    <div class="progress">
                        <div class="progress-fill"></div>
                    </div>

                    <p>{{ readiness.message }}</p>
                </div>

                <h2>Skills Found in Resume</h2>

                {% if found_skills %}
                    {% for skill in found_skills %}
                        <span class="skill">{{ skill }}</span>
                    {% endfor %}
                {% else %}
                    <p>No matching skills found in the resume.</p>
                {% endif %}

                <h2>Available Required Skills</h2>

                {% if available %}
                    {% for skill in available %}
                        <span class="skill">{{ skill }}</span>
                    {% endfor %}
                {% else %}
                    <p>No required skills matched.</p>
                {% endif %}

                <h2>Missing Skills - Learning Recommendations</h2>

                {% if missing %}
                    {% for skill in missing %}
                        <span class="skill missing">{{ skill }}</span>
                    {% endfor %}
                {% else %}
                    <p>All listed skills for this role were found!</p>
                {% endif %}

                <h2>Recommended Job Roles</h2>

                <p>Job roles ranked according to resume skill matches:</p>

                {% for item in recommendations %}
                    <div class="job-card">
                        <h3>{{ item.role }}</h3>

                        <p class="match">
                            {{ item.match }}% Skill Match
                        </p>

                        <p>
                            <b>Matching Skills:</b>
                            {% if item.matched_skills %}
                                {{ item.matched_skills | join(", ") }}
                            {% else %}
                                No matching skills yet
                            {% endif %}
                        </p>
                    </div>
                {% endfor %}

                <div class="note">
                    <b>Important Note:</b>
                    This is a rule-based educational prototype.
                    Readiness is calculated from the selected role's
                    skill match percentage. It is not a trained ML
                    placement prediction model and does not guarantee
                    employment or placement.
                </div>

                <a href="/">Analyze Another Resume</a>

            </div>
        </body>
        </html>
        """

        return render_template_string(
            result_html,
            filename=filename,
            job_role=job_role,
            found_skills=found_skills,
            available=available,
            missing=missing,
            percentage=percentage,
            recommendations=recommendations,
            readiness=readiness
        )

    except Exception:
        app.logger.exception("Resume analysis failed")
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
