from pydantic import BaseModel, Field


class TextMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    job_description: str = Field(..., min_length=50)


class MatchResponse(BaseModel):
    score: float = Field(..., description="Overall match, 0-100")
    verdict: str
    semantic_score: float = Field(..., description="Embedding similarity, 0-100")
    skill_score: float = Field(..., description="% of job skills found in resume")
    matched_skills: list[str]
    missing_skills: list[str]
