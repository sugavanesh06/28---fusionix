from app.database import SessionLocal
from app.models.resume import Resume
from app.models.task import Task
from app.models.task_submission import TaskSubmission
from app.models.project import Project
from app.models.job import Job
from app.models.interview_session import InterviewSession

print('session start')
db=SessionLocal()
user_id=11
resume=db.query(Resume).filter(Resume.user_id==user_id).first()
print('resume',resume)
print('type',type(resume))
print('skills',getattr(resume,'skills',None))
print('missing',getattr(resume,'missing_skills',None))
skills = resume.skills.split(",") if resume and resume.skills else []
missing_skills = resume.missing_skills.split(",") if resume and resume.missing_skills else []
print('lists',skills,missing_skills)
print('tasks count',db.query(Task).filter(Task.user_id==user_id).count())
print('completed tasks',db.query(Task).filter(Task.user_id==user_id, Task.status=='completed').count())
print('jobs count',db.query(Job).count())
print('finished')
db.close()
