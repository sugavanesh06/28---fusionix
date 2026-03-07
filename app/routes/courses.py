from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.services.course_service import get_recommended_courses
from app.models.resume import Resume

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/courses")
def get_courses(credentials=Depends(security), db: Session = Depends(get_db)):
    """Get recommended courses based on user's missing skills"""
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Get missing skills from resume
    missing_skills = resume.missing_skills.split(",") if resume.missing_skills else []
    missing_skills = [s.strip() for s in missing_skills if s.strip()]

    courses = get_recommended_courses(db, missing_skills)

    return {
        "recommended_courses": courses,
        "total_courses": len(courses),
        "target_skills": missing_skills
    }
