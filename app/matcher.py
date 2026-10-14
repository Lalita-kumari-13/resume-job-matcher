"""Core matching logic: semantic similarity (embeddings) + skill overlap."""
from functools import lru_cache

import numpy as np

from .skills import extract_skills

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SEMANTIC_WEIGHT = 0.6
SKILL_WEIGHT = 0.4


@lru_cache(maxsize=1)
def get_model():
    # Imported lazily so tests / startup don't pay the cost until needed.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def chunk_text(text: str, size: int = 120) -> list[str]:
    """MiniLM truncates long input, so embed the text in word chunks."""
    words = text.split()
    return [" ".join(words[i : i + size]) for i in range(0, len(words), size)] or [""]


def semantic_similarity(resume_text: str, job_text: str) -> float:
    """For each job-description chunk, find its best-matching resume chunk,
    then average. Returns cosine similarity in [0, 1]."""
    model = get_model()
    r = model.encode(chunk_text(resume_text), normalize_embeddings=True)
    j = model.encode(chunk_text(job_text), normalize_embeddings=True)
    sims = j @ r.T
    return float(np.clip(sims.max(axis=1).mean(), 0.0, 1.0))


def _rescale(sim: float, low: float = 0.2, high: float = 0.7) -> float:
    """Raw MiniLM cosine for related texts is ~0.3-0.6; stretch to 0-1."""
    return float(np.clip((sim - low) / (high - low), 0.0, 1.0))


def verdict(score: float) -> str:
    if score >= 75:
        return "Strong match"
    if score >= 50:
        return "Moderate match"
    return "Weak match"


def match(resume_text: str, job_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    skill_score = len(matched) / len(job_skills) if job_skills else 0.0
    semantic_score = _rescale(semantic_similarity(resume_text, job_text))

    final = 100 * (SEMANTIC_WEIGHT * semantic_score + SKILL_WEIGHT * skill_score)
    return {
        "score": round(final, 1),
        "verdict": verdict(final),
        "semantic_score": round(100 * semantic_score, 1),
        "skill_score": round(100 * skill_score, 1),
        "matched_skills": matched,
        "missing_skills": missing,
    }
