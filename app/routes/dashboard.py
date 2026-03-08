from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import HTTPBearer, verify_token
from app.models.resume import Resume
from app.models.task import Task
from app.models.task_submission import TaskSubmission
from app.models.project import Project
from app.models.job import Job
from app.models.interview_session import InterviewSession

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard")
def get_dashboard(credentials=Depends(security), db: Session = Depends(get_db)):

    payload = verify_token(credentials.credentials)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload.get("sub"))

    # Resume
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()

    skills = resume.skills.split(",") if resume and resume.skills else []
    missing_skills = resume.missing_skills.split(",") if resume and resume.missing_skills else []

    skills_found_count = len([s for s in skills if s.strip()])
    missing_skills_count = len([s for s in missing_skills if s.strip()])

    total_skill_items = skills_found_count + missing_skills_count
    if total_skill_items > 0:
        skills_score = round((skills_found_count / total_skill_items) * 100)
    else:
        skills_score = 0

    # Tasks (current user only)
    total_tasks = db.query(Task).filter(Task.user_id == user_id).count()

    completed_tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.status == "completed"
    ).count()

    approved_tasks = db.query(TaskSubmission).filter(
        TaskSubmission.user_id == user_id,
        TaskSubmission.status == "approved"
    ).count()

    needs_improvement_tasks = db.query(TaskSubmission).filter(
        TaskSubmission.user_id == user_id,
        TaskSubmission.status == "needs_improvement"
    ).count()

    pending_tasks = max(total_tasks - approved_tasks - needs_improvement_tasks, 0)

    # Calculate tasks score based on completed MCQ tasks
    if total_tasks > 0:
        tasks_score = round((completed_tasks / total_tasks) * 100)
    else:
        tasks_score = 0

    # Projects
    total_projects = db.query(Project).filter(Project.user_id == user_id).count()

    approved_projects = db.query(Project).filter(
        Project.user_id == user_id,
        Project.status == "approved"
    ).count()

    needs_improvement_projects = db.query(Project).filter(
        Project.user_id == user_id,
        Project.status == "needs_improvement"
    ).count()

    if total_projects > 0:
        projects_score = round((approved_projects / total_projects) * 100)
    else:
        projects_score = 0

    # Jobs
    jobs = db.query(Job).count()

    # Interview
    completed_interviews = db.query(InterviewSession).filter(
        InterviewSession.user_id == user_id,
        InterviewSession.status == "completed"
    ).all()

    if completed_interviews:
        interview_scores = []
        for interview in completed_interviews:
            if interview.question_count and interview.question_count > 0:
                avg_score = (interview.total_score / interview.question_count) * 10
                interview_scores.append(avg_score)

        interview_score = round(sum(interview_scores) / len(interview_scores)) if interview_scores else 0
    else:
        interview_score = 0

    # Overall readiness score
    career_readiness_score = round(
        (skills_score * 0.30) +
        (tasks_score * 0.25) +
        (projects_score * 0.20) +
        (interview_score * 0.25)
    )

    return {
        "skills_summary": {
            "skills_found": skills_found_count,
            "missing_skills": missing_skills_count,
            "skills_score": skills_score,
            "skills_list": skills,
            "missing_skills_list": missing_skills
        },

        "task_summary": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "approved_tasks": approved_tasks,
            "needs_improvement_tasks": needs_improvement_tasks,
            "pending_tasks": pending_tasks,
            "tasks_score": tasks_score
        },

        "project_summary": {
            "total_projects": total_projects,
            "approved_projects": approved_projects,
            "needs_improvement_projects": needs_improvement_projects,
            "projects_score": projects_score
        },

        "interview_summary": {
            "completed_interviews": len(completed_interviews),
            "interview_score": interview_score
        },

        "job_summary": {
            "available_jobs": jobs
        },

        "career_readiness_score": career_readiness_score
    }