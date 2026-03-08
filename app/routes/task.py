from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.services.validation_service import submit_and_validate_task
from app.services.task_service import (
    get_mcqs_for_user,
    complete_task,
    get_task_completion_stats
)
from app.models.task import Task

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks")
def get_tasks(credentials=Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "week": t.week,
                "task_title": t.task_title,
                "task_description": t.task_description,
                "skill": t.skill,
                "status": t.status
            }
            for t in tasks
        ]
    }

@router.post("/tasks/submit")
def submit_task(data: dict, credentials=Depends(security), db: Session = Depends(get_db)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    result = submit_and_validate_task(
        db=db,
        user_id=user_id,
        task_id=data.get("task_id"),
        submission_text=data.get("submission_text"),
        github_link=data.get("github_link")
    )

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    return result


@router.get("/mcqs")
def get_mcqs(credentials=Depends(security), db: Session = Depends(get_db)):
    """Get MCQs for the current week"""
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))
    result = get_mcqs_for_user(db, user_id)
    
    return result


@router.post("/tasks/complete")
def complete_task_endpoint(
    data: dict = Body(...),
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    """Mark a task as completed"""
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))
    task_id = data.get("task_id")
    task_type = data.get("task_type", "mcq")
    selected_option = data.get("selected_option")
    correct_option = data.get("correct_option")

    if not task_id:
        raise HTTPException(status_code=400, detail="task_id is required")

    result = complete_task(db, user_id, task_id, task_type, selected_option, correct_option)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.get("/tasks/stats")
def get_stats(credentials=Depends(security), db: Session = Depends(get_db)):
    """Get task completion statistics"""
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))
    stats = get_task_completion_stats(db, user_id)
    
    return stats