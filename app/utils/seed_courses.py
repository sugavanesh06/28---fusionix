from app.database import SessionLocal
from app.models.course import Course

db = SessionLocal()

sample_courses = [
    # React courses
    {"title": "React for Beginners", "skill": "React", "platform": "Udemy", "link": "https://udemy.com/react", "price": "499", "rating": "4.5", "is_sponsored": True},
    {"title": "React Crash Course", "skill": "React", "platform": "YouTube", "link": "https://youtube.com/react", "price": "Free", "rating": "4.3", "is_sponsored": False},
    {"title": "Advanced React Patterns", "skill": "React", "platform": "Pluralsight", "link": "https://pluralsight.com/react", "price": "29/month", "rating": "4.6", "is_sponsored": False},
    
    # Node.js courses
    {"title": "Node.js Complete Guide", "skill": "Node.js", "platform": "Coursera", "link": "https://coursera.com/node", "price": "Free", "rating": "4.6", "is_sponsored": False},
    {"title": "Express.js for Backend Development", "skill": "Node.js", "platform": "Udemy", "link": "https://udemy.com/express", "price": "599", "rating": "4.5", "is_sponsored": True},
    {"title": "Building APIs with Node.js", "skill": "Node.js", "platform": "YouTube", "link": "https://youtube.com/nodejs", "price": "Free", "rating": "4.4", "is_sponsored": False},
    
    # MongoDB courses
    {"title": "MongoDB Basics", "skill": "MongoDB", "platform": "YouTube", "link": "https://youtube.com/mongodb", "price": "Free", "rating": "4.4", "is_sponsored": False},
    {"title": "MongoDB University", "skill": "MongoDB", "platform": "MongoDB", "link": "https://university.mongodb.com", "price": "Free", "rating": "4.7", "is_sponsored": True},
    {"title": "MongoDB Advanced", "skill": "MongoDB", "platform": "Udemy", "link": "https://udemy.com/mongodb", "price": "499", "rating": "4.5", "is_sponsored": False},
    
    # TypeScript courses
    {"title": "TypeScript for Beginners", "skill": "TypeScript", "platform": "Udemy", "link": "https://udemy.com/typescript", "price": "599", "rating": "4.6", "is_sponsored": True},
    {"title": "TypeScript Handbook", "skill": "TypeScript", "platform": "Official", "link": "https://typescriptlang.org", "price": "Free", "rating": "4.8", "is_sponsored": False},
    
    # Docker courses
    {"title": "Docker Fundamentals", "skill": "Docker", "platform": "Udemy", "link": "https://udemy.com/docker", "price": "499", "rating": "4.5", "is_sponsored": True},
    {"title": "Docker Crash Course", "skill": "Docker", "platform": "YouTube", "link": "https://youtube.com/docker", "price": "Free", "rating": "4.4", "is_sponsored": False},
    
    # Kubernetes courses
    {"title": "Kubernetes for Beginners", "skill": "Kubernetes", "platform": "Udemy", "link": "https://udemy.com/kubernetes", "price": "599", "rating": "4.5", "is_sponsored": True},
    {"title": "Kubernetes Crash Course", "skill": "Kubernetes", "platform": "YouTube", "link": "https://youtube.com/kubernetes", "price": "Free", "rating": "4.3", "is_sponsored": False},
    
    # SQL courses
    {"title": "SQL Fundamentals", "skill": "SQL", "platform": "Udemy", "link": "https://udemy.com/sql", "price": "399", "rating": "4.6", "is_sponsored": False},
    {"title": "SQL Complete Course", "skill": "SQL", "platform": "Coursera", "link": "https://coursera.com/sql", "price": "Free", "rating": "4.5", "is_sponsored": False},
    
    # AWS courses
    {"title": "AWS for Beginners", "skill": "AWS", "platform": "Udemy", "link": "https://udemy.com/aws", "price": "699", "rating": "4.5", "is_sponsored": True},
    {"title": "AWS Certified Associate", "skill": "AWS", "platform": "Linux Academy", "link": "https://linuxacademy.com/aws", "price": "29/month", "rating": "4.6", "is_sponsored": False},
    
    # Python courses
    {"title": "Python for Data Science", "skill": "Python", "platform": "Udemy", "link": "https://udemy.com/python", "price": "499", "rating": "4.5", "is_sponsored": True},
    {"title": "Python Advanced", "skill": "Python", "platform": "YouTube", "link": "https://youtube.com/python", "price": "Free", "rating": "4.4", "is_sponsored": False},
    
    # REST APIs courses
    {"title": "RESTful API Design", "skill": "REST APIs", "platform": "Udemy", "link": "https://udemy.com/rest", "price": "599", "rating": "4.5", "is_sponsored": True},
    {"title": "API Development Guide", "skill": "REST APIs", "platform": "YouTube", "link": "https://youtube.com/api", "price": "Free", "rating": "4.3", "is_sponsored": False},
    
    # CI/CD courses
    {"title": "CI/CD Pipeline Mastery", "skill": "CI/CD", "platform": "Udemy", "link": "https://udemy.com/cicd", "price": "599", "rating": "4.5", "is_sponsored": True},
    {"title": "GitHub Actions Guide", "skill": "CI/CD", "platform": "YouTube", "link": "https://youtube.com/github-actions", "price": "Free", "rating": "4.4", "is_sponsored": False},
]

for item in sample_courses:
    exists = db.query(Course).filter(
        Course.title == item["title"],
        Course.skill == item["skill"]
    ).first()

    if not exists:
        db.add(Course(**item))

db.commit()
db.close()

print("Courses seeded successfully!")