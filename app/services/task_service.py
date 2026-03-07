from datetime import datetime
from sqlalchemy import func
from app.agents.task_agent import generate_daily_tasks
from app.models.task import Task
from app.models.resume import Resume
from app.agents.mcq_agent import generate_mcqs


def create_tasks_from_roadmap(db, user_id, goal, roadmap, week="week1"):
    if "detailed_roadmap" not in roadmap or week not in roadmap["detailed_roadmap"]:
        return []

    week_data = roadmap["detailed_roadmap"][week]
    generated = generate_daily_tasks(goal, week, week_data)

    created_tasks = []

    for item in generated.get("tasks", []):
        task = Task(
            user_id=user_id,
            week=week,
            task_title=item.get("task_title"),
            task_description=item.get("task_description"),
            skill=item.get("skill"),
            status="pending"
        )
        db.add(task)
        created_tasks.append(task)

    db.commit()

    return [
        {
            "task_title": t.task_title,
            "task_description": t.task_description,
            "skill": t.skill,
            "status": t.status
        }
        for t in created_tasks
    ]


def get_mcqs_for_user(db, user_id):
    """
    Get MCQs for the current week based on user's roadmap
    """
    # Get user's resume to find roadmap and current week
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    
    # For now, assume week 1 is the current week
    # In production, you would track the current week in the database
    current_week = 1
    
    # Parse roadmap from resume or use roadmap stored separately
    # For this implementation, we'll generate MCQs based on common week themes
    week_themes = {
        1: "HTML & CSS Foundations",
        2: "JavaScript Fundamentals",
        3: "React Basics",
        4: "Advanced React",
        5: "State Management",
        6: "API Integration",
        7: "Testing & Debugging",
        8: "Deployment & Optimization"
    }
    
    week_projects = {
        1: "Complete responsive portfolio website with contact form and project showcase",
        2: "Interactive web application with dynamic content and user interactions",
        3: "Full-featured React application with routing and state management",
        4: "Complex React application with advanced patterns and optimizations",
        5: "Scalable application with complex state logic and data flow",
        6: "Full-stack application with backend API and frontend client",
        7: "Production-ready application with comprehensive test coverage",
        8: "Optimized, deployed application with monitoring and analytics"
    }
    
    week_theme = week_themes.get(current_week, "Learning")
    week_project = week_projects.get(current_week, "Complete your learning task")
    
    # Parse missing skills from resume if available
    missing_skills = []
    if resume and resume.missing_skills:
        missing_skills = [s.strip() for s in resume.missing_skills.split(',') if s.strip()][:3]
    
    # Generate MCQs
    tasks = generate_mcqs(current_week, week_theme, week_project, missing_skills)
    
    return {
        "tasks": tasks,
        "week": current_week,
        "theme": week_theme,
        "project": week_project
    }


def complete_task(db, user_id, task_id, task_type, selected_option=None, correct_option=None):
    """
    Mark a task as completed
    """
    from datetime import datetime
    
    task = db.query(Task).filter(
        Task.user_id == user_id,
        Task.id == task_id
    ).first()
    
    # If task doesn't exist, create it (for transient MCQ tasks)
    if not task:
        task = Task(
            user_id=user_id,
            week="week1",
            task_title=f"MCQ Task {task_id}",
            task_description="Daily MCQ Task",
            skill="General",
            status="completed"
        )
        db.add(task)
    else:
        task.status = "completed"
    
    # Calculate score for MCQ
    score = 0
    is_correct = False
    if task_type == "mcq" and selected_option is not None and correct_option is not None:
        is_correct = selected_option == correct_option
        score = 1 if is_correct else 0.5
    else:
        score = 1
        is_correct = True
    
    task.completed_at = datetime.utcnow()
    # assign score only if attribute exists (in case table not yet migrated)
    if hasattr(task, 'score'):
        task.score = score
    
    try:
        db.commit()
    except Exception as e:
        # log but don't crash
        import traceback
        print(f"Warning: DB commit failed in complete_task: {e}")
        traceback.print_exc()
        db.rollback()

    return {
        "message": "Task completed successfully",
        "score": score,
        "is_correct": is_correct
    }

# end of complete_task
    
    return {
        "message": "Task completed successfully",
        "score": score,
        "is_correct": is_correct
    }


def get_task_completion_stats(db, user_id):
    """
    Get task completion statistics for the user
    """
    total_tasks = db.query(func.count(Task.id)).filter(
        Task.user_id == user_id
    ).scalar() or 0
    
    completed_tasks = db.query(func.count(Task.id)).filter(
        Task.user_id == user_id,
        Task.status == "completed"
    ).scalar() or 0
    
    correct_tasks = db.query(func.count(Task.id)).filter(
        Task.user_id == user_id,
        Task.status == "completed",
        Task.score >= 0.9
    ).scalar() or 0
    
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "correct_tasks": correct_tasks,
        "completion_percentage": round(completion_percentage, 1)
    }