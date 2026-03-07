from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.services.project_service import submit_project

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/projects/submit")
def create_project(data: dict, credentials=Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    result = submit_project(
        db=db,
        user_id=user_id,
        project_name=data.get("project_name"),
        description=data.get("description"),
        github_link=data.get("github_link"),
        live_link=data.get("live_link")
    )

    return result