from fastapi import APIRouter, HTTPException
from backend.database import get_companies

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.get("/")
def get_all_companies():
    try:
        return get_companies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
