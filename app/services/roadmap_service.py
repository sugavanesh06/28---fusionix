from app.agents.roadmap_agent import generate_roadmap

def create_roadmap(goal, skills, missing_skills):

    roadmap = generate_roadmap(goal, skills, missing_skills)

    return roadmap