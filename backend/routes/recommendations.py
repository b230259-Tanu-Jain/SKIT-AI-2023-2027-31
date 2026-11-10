import pandas as pd
from fastapi import APIRouter, HTTPException
from backend.database import get_companies, get_job_roles
from backend.schemas.recommendation import RecommendationRequest
from features.recommendation.user_profile import UserProfile
from features.recommendation.recommendation import (
    recommend_companies,
    recommend_job_roles
)
router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)
def create_profile(data):
    return UserProfile(
        skills=data.skills,
        work_life_balance=data.work_life_balance,
        culture_values=data.culture_values,
        career_opp=data.career_opp,
        comp_benefits=data.comp_benefits
    )
@router.post("/companies")
def company_recommendations(data: RecommendationRequest):
    try:
        profile = create_profile(data)
        df = pd.DataFrame(get_companies())

        if df.empty:
            return []

        results = recommend_companies(df, profile, top_n=5)
        return results.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/job-roles")
def job_role_recommendations(data: RecommendationRequest):
    try:
        profile = create_profile(data)
        df = pd.DataFrame(get_job_roles())

        if df.empty:
            return []

        results = recommend_job_roles(df, profile, top_n=5)
        return results.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))