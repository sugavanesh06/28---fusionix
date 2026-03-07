from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class TaskSubmission(Base):
    __tablename__ = "task_submissions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    submission_text = Column(Text, nullable=True)
    github_link = Column(String(500), nullable=True)
    score = Column(String(20), nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String(50), default="submitted")