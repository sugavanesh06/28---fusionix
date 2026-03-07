from app.models.project import Project
from app.agents.project_agent import validate_project

def submit_project(db, user_id, project_name, description, github_link, live_link):
    result = validate_project(project_name, description, github_link, live_link)

    project = Project(
        user_id=user_id,
        project_name=project_name,
        description=description,
        github_link=github_link,
        live_link=live_link,
        score=result.get("score"),
        feedback=result.get("feedback"),
        status=result.get("status")
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "project_name": project.project_name,
        "score": project.score,
        "feedback": project.feedback,
        "status": project.status
    }