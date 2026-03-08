from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.services.job_service import get_job_recommendations
from app.models.resume import Resume

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/jobs")
def get_jobs(credentials=Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Use missing_skills to find relevant jobs, or fall back to current skills
    missing_skills = resume.missing_skills.split(",") if resume.missing_skills else []
    current_skills = resume.skills.split(",") if resume.skills else []
    
    # Prioritize missing skills for job recommendations
    search_skills = missing_skills if missing_skills else current_skills

    jobs = get_job_recommendations(db, search_skills)

    return {
        "recommended_jobs": jobs
    }