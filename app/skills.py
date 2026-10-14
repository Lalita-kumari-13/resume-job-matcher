"""Skill taxonomy + extraction. Canonical skill -> aliases found in text."""
import re

SKILL_ALIASES: dict[str, list[str]] = {
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],
    "c++": ["c++"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "spring boot": ["spring boot", "springboot"],
    "rest api": ["rest api", "rest apis", "restful"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "generative ai": ["generative ai", "genai", "llm", "llms"],
    "rag": ["rag", "retrieval-augmented generation"],
    "langchain": ["langchain"],
    "transformers": ["transformers", "hugging face", "huggingface"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "embeddings": ["embeddings", "embedding"],
    "vector database": ["faiss", "chromadb", "pinecone", "vector database"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github"],
    "ci/cd": ["ci/cd", "github actions", "jenkins"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "data structures": ["data structures", "dsa"],
    "oop": ["oop", "object-oriented"],
    "streamlit": ["streamlit"],
    "linux": ["linux"],
    "testing": ["pytest", "unit testing", "junit"],
}


def _pattern(alias: str) -> re.Pattern:
    return re.compile(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", re.IGNORECASE)


_PATTERNS = {
    skill: [_pattern(a) for a in aliases] for skill, aliases in SKILL_ALIASES.items()
}


def extract_skills(text: str) -> set[str]:
    """Return the set of canonical skills mentioned in `text`."""
    return {
        skill
        for skill, patterns in _PATTERNS.items()
        if any(p.search(text) for p in patterns)
    }
