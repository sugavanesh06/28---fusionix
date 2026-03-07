from app.database import SessionLocal
from app.models.job import Job

db = SessionLocal()

jobs = [
    # Frontend Developer Jobs
    {"title": "Frontend Developer", "company": "TechCorp", "location": "Bangalore", "salary": "6 LPA", "required_skills": "React,JavaScript,HTML,CSS", "link": "https://example.com/job1"},
    {"title": "React Developer", "company": "StartupX", "location": "Remote", "salary": "7 LPA", "required_skills": "React,JavaScript,TypeScript", "link": "https://example.com/job2"},
    {"title": "Senior Frontend Engineer", "company": "WebSolutions", "location": "Mumbai", "salary": "12 LPA", "required_skills": "React,Vue.js,JavaScript,CSS", "link": "https://example.com/job3"},
    
    # Backend Developer Jobs
    {"title": "Backend Developer", "company": "CloudSys", "location": "Hyderabad", "salary": "7 LPA", "required_skills": "Node.js,Python,SQL,Docker", "link": "https://example.com/job4"},
    {"title": "Node.js Developer", "company": "APIWorks", "location": "Remote", "salary": "8 LPA", "required_skills": "Node.js,Express,MongoDB,REST APIs", "link": "https://example.com/job5"},
    {"title": "Full Stack Developer", "company": "DevWorks", "location": "Chennai", "salary": "8 LPA", "required_skills": "React,Node.js,MongoDB,Docker", "link": "https://example.com/job6"},
    
    # Database Jobs
    {"title": "Database Administrator", "company": "DataCore", "location": "Bangalore", "salary": "7 LPA", "required_skills": "SQL,PostgreSQL,MongoDB,AWS", "link": "https://example.com/job7"},
    {"title": "Data Engineer", "company": "BigData Inc", "location": "Pune", "salary": "9 LPA", "required_skills": "SQL,Python,Spark,Docker", "link": "https://example.com/job8"},
    
    # DevOps Jobs
    {"title": "DevOps Engineer", "company": "InfraSys", "location": "Remote", "salary": "9 LPA", "required_skills": "Docker,Kubernetes,CI/CD,AWS", "link": "https://example.com/job9"},
    {"title": "Cloud Architect", "company": "CloudPro", "location": "Bangalore", "salary": "10 LPA", "required_skills": "AWS,Kubernetes,Docker,Terraform", "link": "https://example.com/job10"},
    
    # TypeScript Jobs
    {"title": "TypeScript Developer", "company": "CodeBase", "location": "Remote", "salary": "8 LPA", "required_skills": "TypeScript,React,Node.js,REST APIs", "link": "https://example.com/job11"},
    {"title": "Senior TypeScript Engineer", "company": "TechLead", "location": "Bangalore", "salary": "11 LPA", "required_skills": "TypeScript,React,Kubernetes,Docker", "link": "https://example.com/job12"},
    
    # Python Jobs
    {"title": "Python Developer", "company": "PyTech", "location": "Remote", "salary": "7 LPA", "required_skills": "Python,SQL,Django,REST APIs", "link": "https://example.com/job13"},
    {"title": "Machine Learning Engineer", "company": "AI Labs", "location": "Bangalore", "salary": "10 LPA", "required_skills": "Python,TensorFlow,SQL,Statistics", "link": "https://example.com/job14"},
    
    # Microservices Jobs
    {"title": "Microservices Architect", "company": "ArchSys", "location": "Bangalore", "salary": "12 LPA", "required_skills": "Microservices,Docker,Kubernetes,REST APIs", "link": "https://example.com/job15"},
    
    # Full Stack with Advanced Tech
    {"title": "Full Stack Engineer", "company": "ModernTech", "location": "Remote", "salary": "9 LPA", "required_skills": "React,Node.js,PostgreSQL,Docker,CI/CD", "link": "https://example.com/job16"},
    {"title": "Senior Full Stack", "company": "EnterpriseSys", "location": "Mumbai", "salary": "13 LPA", "required_skills": "React,Node.js,SQL,Kubernetes,AWS", "link": "https://example.com/job17"},
]

for j in jobs:
    exists = db.query(Job).filter(
        Job.title == j["title"],
        Job.company == j["company"]
    ).first()
    
    if not exists:
        job = Job(**j)
        db.add(job)

db.commit()
db.close()

print("Jobs seeded successfully")