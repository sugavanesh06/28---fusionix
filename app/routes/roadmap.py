from fastapi import APIRouter
from app.services.roadmap_service import create_roadmap

router = APIRouter()

@router.post("/roadmap")
def generate_user_roadmap(data: dict):

    goal = data.get("goal")
    skills = data.get("skills")
    missing_skills = data.get("missing_skills")

    roadmap = create_roadmap(goal, skills, missing_skills)

    return {
        "roadmap": roadmap
    }