
from app import app
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
            "resume": (io.BytesIO(b"sample content"), "resume.txt")
        },
        content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert b"Only PDF and DOCX" in response.data
