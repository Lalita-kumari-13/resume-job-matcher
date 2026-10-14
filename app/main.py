from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from . import matcher
from .parser import extract_text_from_pdf
from .schemas import MatchResponse, TextMatchRequest

MAX_PDF_BYTES = 5 * 1024 * 1024

app = FastAPI(
    title="AI Resume-Job Matcher",
    description="Scores how well a resume fits a job description using "
    "sentence embeddings + skill-gap analysis.",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/match/text", response_model=MatchResponse)
def match_text(body: TextMatchRequest):
    return matcher.match(body.resume_text, body.job_description)


@app.post("/match", response_model=MatchResponse)
async def match_pdf(
    resume: UploadFile = File(..., description="Resume as PDF"),
    job_description: str = Form(..., min_length=50),
):
    if not (resume.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Resume must be a PDF file.")
    data = await resume.read()
    if len(data) > MAX_PDF_BYTES:
        raise HTTPException(413, "PDF too large (max 5 MB).")
    try:
        text = extract_text_from_pdf(data)
    except Exception:
        raise HTTPException(400, "Could not read the PDF.")
    if len(text) < 50:
        raise HTTPException(422, "No readable text found (scanned PDF?).")
    return matcher.match(text, job_description)
