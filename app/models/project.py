from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_name = Column(String(255), nullable=False)
    github_link = Column(String(500), nullable=True)
    live_link = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    score = Column(String(20), nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String(50), default="submitted")