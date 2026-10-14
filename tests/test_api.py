from fastapi.testclient import TestClient

from app import matcher
from app.main import app

client = TestClient(app)

RESUME = "Python developer with FastAPI, scikit-learn and MongoDB experience. " * 3
JD = "We need a Python engineer with FastAPI, Docker and Kubernetes skills. " * 3


def _fake_similarity(a, b):
    return 0.6  # avoid downloading the embedding model in tests


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_match_text(monkeypatch):
    monkeypatch.setattr(matcher, "semantic_similarity", _fake_similarity)
    r = client.post("/match/text", json={"resume_text": RESUME, "job_description": JD})
    assert r.status_code == 200
    body = r.json()
    assert "python" in body["matched_skills"]
    assert {"docker", "kubernetes"} <= set(body["missing_skills"])
    assert 0 <= body["score"] <= 100


def test_rejects_non_pdf():
    r = client.post(
        "/match",
        files={"resume": ("cv.txt", b"hello", "text/plain")},
        data={"job_description": JD},
    )
    assert r.status_code == 400


def test_validation_error_on_short_input():
    r = client.post("/match/text", json={"resume_text": "hi", "job_description": "yo"})
    assert r.status_code == 422
