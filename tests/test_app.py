
from app import app, analyze_skill_gap
import io


def test_homepage():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Placement Intelligence System" in response.data


def test_health_api():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_invalid_resume_file():
    response = app.test_client().post(
        "/upload-resume",
        data={
            "resume": (io.BytesIO(b"sample content"), "resume.txt"),
            "job_role": "Data Analyst"
        },
        content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert b"Only PDF and DOCX" in response.data


def test_skill_gap_analysis():
    found_skills = ["Python", "SQL", "Excel"]

    available, missing, percentage = analyze_skill_gap(
        found_skills, "Data Analyst"
    )

    assert available == ["Python", "SQL", "Excel"]
    assert "Power BI" in missing
    assert "Data Analytics" in missing
    assert percentage == 60
