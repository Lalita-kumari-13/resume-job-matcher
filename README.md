# 🎯 AI Resume-Job Matcher

Upload a resume (PDF), paste a job description, and get an explainable **fit score**, matched skills, and a **skill-gap report**.

## How it works

1. **Parse** – text is extracted from the PDF (`pypdf`).
2. **Semantic similarity** – resume and JD are split into chunks and embedded with `all-MiniLM-L6-v2` (Sentence-Transformers). Each JD chunk is matched to its closest resume chunk via cosine similarity, then averaged.
3. **Skill analysis** – a skill taxonomy (with aliases, e.g. `sklearn` → `scikit-learn`) is matched against both texts to find matched and missing skills.
4. **Final score** = `60% semantic similarity + 40% skill coverage`, mapped to *Strong / Moderate / Weak*.

```
Streamlit UI ──HTTP──► FastAPI (/match) ──► parser ─► matcher (embeddings + skills)
```

## Tech stack
Python · FastAPI · Sentence-Transformers · NumPy · Streamlit · pypdf · Pydantic · Pytest · Docker · GitHub Actions

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

uvicorn app.main:app --reload          # API  → http://localhost:8000/docs
streamlit run streamlit_app.py         # UI   → http://localhost:8501
```

## Run with Docker

```bash
docker build -t resume-matcher .
docker run -p 8000:8000 resume-matcher
```

## API

`POST /match` (multipart: `resume` PDF + `job_description`)

```bash
curl -X POST http://localhost:8000/match \
  -F "resume=@resume.pdf" \
  -F "job_description=We are hiring a Python AI engineer with FastAPI, Docker and NLP experience..."
```

```json
{
  "score": 68.4,
  "verdict": "Moderate match",
  "semantic_score": 72.1,
  "skill_score": 62.5,
  "matched_skills": ["fastapi", "nlp", "python"],
  "missing_skills": ["docker", "kubernetes"]
}
```

Also: `POST /match/text` (JSON), `GET /health`. Interactive docs at `/docs`.

## Tests

```bash
pytest -q
```

## Design notes & limitations
- Skill extraction is dictionary-based (fast, explainable) – it won't catch skills outside the taxonomy in `app/skills.py`.
- Scores are a heuristic, not a hiring decision. Raw MiniLM similarities are rescaled to a 0–1 range for readability.
- Scanned (image-only) PDFs are rejected; OCR is a possible extension.

## Roadmap
- [ ] Rank one resume against many job descriptions
- [ ] LLM-generated resume improvement suggestions
- [ ] Persist history in MongoDB
- [ ] Deploy API (Render) + UI (Streamlit Community Cloud)
