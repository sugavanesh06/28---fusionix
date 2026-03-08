from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    role = Column(String(100), nullable=False)
    current_question = Column(Text, nullable=True)
    question_count = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    status = Column(String(50), default="active")
    started_at = Column(DateTime, default=datetime.utcnow)