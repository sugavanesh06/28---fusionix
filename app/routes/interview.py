from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.services.interview_service import start_interview, answer_interview

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/interview/start")
def begin_interview(
    data: dict = Body(...),
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))
    role = data.get("role")

    if not role:
        raise HTTPException(status_code=400, detail="Role is required")

    return start_interview(db, user_id, role)


@router.post("/interview/answer")
def submit_interview_answer(
    data: dict = Body(...),
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session_id = data.get("session_id")
    answer = data.get("answer")

    if not session_id or not answer:
        raise HTTPException(status_code=400, detail="session_id and answer are required")

    result = answer_interview(db, session_id, answer)

    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return result