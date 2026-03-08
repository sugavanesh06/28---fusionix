from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import Base, engine, SessionLocal

# Import routes
from app.routes import auth, resume, roadmap, task, project, job, dashboard, interview, courses

# Import models so tables are created
from app.models.course import Course
from app.models.task import Task
from app.models.project import Project
from app.models.task_submission import TaskSubmission
from app.models.job import Job
from app.models.interview_session import InterviewSession

# Startup event to seed data
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Seed database with jobs and courses on startup
        db = SessionLocal()
        
        # Check if data already exists
        job_count = db.query(Job).count()
        course_count = db.query(Course).count()
        
        if job_count == 0:
            print("Seeding jobs...")
            from app.utils.seed_jobs import jobs
            for j in jobs:
                db.add(Job(**j))
            db.commit()
        
        if course_count < 10:  # Seed if we have less than 10 courses
            print("Seeding courses...")
            from app.utils.seed_courses import sample_courses
            for item in sample_courses:
                exists = db.query(Course).filter(
                    Course.title == item["title"],
                    Course.skill == item["skill"]
                ).first()
                if not exists:
                    db.add(Course(**item))
            db.commit()
        
        db.close()
    except Exception as e:
        print(f"Warning: Data seeding failed: {e}")
    
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)


# -----------------------------
# CORS (Frontend connect panna)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # hackathon ku ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Create tables
# -----------------------------
Base.metadata.create_all(bind=engine)


# -----------------------------
# Routes
# -----------------------------
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(roadmap.router)
app.include_router(task.router)
app.include_router(project.router)
app.include_router(job.router)
app.include_router(courses.router)
app.include_router(dashboard.router)
app.include_router(interview.router)

# Mount static files
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")