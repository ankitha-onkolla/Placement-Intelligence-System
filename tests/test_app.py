
import io

from app import (
    app,
    analyze_skill_gap,
    recommend_jobs,
    predict_placement_readiness,
    generate_learning_roadmap
)


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


def test_job_recommendations():
    found_skills = [
        "Python", "SQL", "Excel", "Power BI", "Data Analytics"
    ]

    recommendations = recommend_jobs(found_skills)

    assert len(recommendations) == 4
    assert recommendations[0]["role"] == "Data Analyst"
    assert recommendations[0]["match"] == 100


def test_placement_readiness_prediction():
    result = predict_placement_readiness(80)

    assert result["score"] == 80
    assert result["status"] == "High Readiness"


def test_learning_roadmap():
    roadmap = generate_learning_roadmap(["SQL", "Machine Learning"])

    assert len(roadmap) == 2
    assert roadmap[0]["skill"] == "SQL"
    assert roadmap[0]["duration"] == "2 weeks"
    assert roadmap[1]["skill"] == "Machine Learning"
