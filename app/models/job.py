from sqlalchemy import Column, Integer, String
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(100), nullable=True)
    salary = Column(String(100), nullable=True)
    required_skills = Column(String(500), nullable=True)
    link = Column(String(500), nullable=True)