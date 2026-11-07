from pydantic import BaseModel, Field

class RecommendationRequest(BaseModel):
    skills: list[str] = Field(default_factory=list)
    work_life_balance: float = Field(70, ge=0, le=100)
    culture_values: float = Field(70, ge=0, le=100)
    career_opp: float = Field(70, ge=0, le=100)
    comp_benefits: float = Field(70, ge=0, le=100)
