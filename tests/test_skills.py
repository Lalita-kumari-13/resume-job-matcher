from app.skills import extract_skills


def test_extracts_known_skills():
    s = extract_skills("Built REST APIs with FastAPI and Python, stored in MongoDB.")
    assert {"python", "fastapi", "rest api", "mongodb"} <= s


def test_java_does_not_match_javascript():
    assert "java" not in extract_skills("Experienced in JavaScript")


def test_case_insensitive_and_aliases():
    assert "scikit-learn" in extract_skills("Used SKLEARN for modelling")
