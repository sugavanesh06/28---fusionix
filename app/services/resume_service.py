
from app.agents.roadmap_agent import generate_roadmap

def process_resume_and_generate_roadmap(resume_text, goal):
    # 1. Resume analyse
    skills = ["HTML", "CSS", "JavaScript"]  # example
    missing_skills = ["React", "Node.js", "MongoDB"]  # example

    # 2. Roadmap generate
    roadmap = generate_roadmap(goal, skills, missing_skills)

    # 3. Return full response
    return {
        "skills": skills,
        "missing_skills": missing_skills,
        "goals": goal,
        "roadmap": roadmap
    }