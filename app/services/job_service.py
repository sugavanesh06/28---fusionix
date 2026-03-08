from app.models.job import Job

def get_job_recommendations(db, skills):
    jobs = db.query(Job).all()

    recommended = []

    for job in jobs:
        job_skills = job.required_skills.split(",") if job.required_skills else []
        match = any(skill.strip() in [js.strip() for js in job_skills] for skill in skills)

        if match:
            recommended.append({
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "salary": job.salary,
                "link": job.link
            })

    return recommended