from app.agents.validation_agent import validate_task
from app.models.task import Task
from app.models.task_submission import TaskSubmission

def submit_and_validate_task(db, user_id, task_id, submission_text, github_link=None):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None

    result = validate_task(task.task_title, task.task_description, submission_text)

    submission = TaskSubmission(
        task_id=task.id,
        user_id=user_id,
        submission_text=submission_text,
        github_link=github_link,
        score=result.get("score"),
        feedback=result.get("feedback"),
        status=result.get("status")
    )
    db.add(submission)

    task.status = result.get("status")
    db.commit()

    return {
        "task_id": task.id,
        "score": result.get("score"),
        "feedback": result.get("feedback"),
        "status": result.get("status")
    }