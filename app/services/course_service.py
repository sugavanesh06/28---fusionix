from sqlalchemy.orm import Session
from app.models.course import Course


def get_recommended_courses(db: Session, missing_skills: list):

    if not missing_skills:
        return []

    courses = (
        db.query(Course)
        .filter(Course.skill.in_(missing_skills))
        .order_by(Course.is_sponsored.desc())
        .all()
    )

    return [
        {
            "title": c.title,
            "skill": c.skill,
            "platform": c.platform,
            "link": c.link,
            "price": c.price,
            "rating": c.rating,
            "is_sponsored": c.is_sponsored
        }
        for c in courses
    ]