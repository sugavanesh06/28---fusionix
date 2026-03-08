from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    skill = Column(String(100), nullable=False)
    platform = Column(String(100), nullable=False)
    link = Column(String(500), nullable=False)
    price = Column(String(50), nullable=True)
    rating = Column(String(20), nullable=True)
    is_sponsored = Column(Boolean, default=False)