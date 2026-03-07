from PyPDF2 import PdfReader
from docx import Document
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client only if API key exists
groq_api_key = os.getenv("GROQ_API_KEY")
client = None
if groq_api_key:
    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
    except Exception as e:
        print(f"Warning: Groq client initialization failed: {e}")

def parse_resume(file_path: str) -> str:
    """
    Takes a file path (PDF, DOCX, or TXT) and returns extracted text.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print("Error reading PDF:", e)

    elif ext in [".docx", ".doc"]:
        try:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print("Error reading DOCX:", e)
    
    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print("Error reading TXT:", e)

    else:
        raise ValueError("Unsupported file format. Only PDF, DOCX, and TXT allowed.")

    return text.strip()

# Common technical skills vocabulary for fallback extraction
COMMON_SKILLS = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust", "php",
    "kotlin", "swift", "objective-c", "scala", "perl", "r", "matlab", "vb", "groovy",
    # Frontend
    "react", "vue", "angular", "html", "css", "sass", "less", "babel", "webpack", "rest",
    # Backend
    "nodejs", "node.js", "express", "fastapi", "django", "flask", "spring", "spring boot",
    # Databases
    "sql", "mysql", "postgres", "mongodb", "cassandra", "redis", "elasticsearch",
    "sqlite", "oracle", "dynamodb", "firestore",
    # DevOps & Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "cicd", "jenkins", "gitlab", "github",
    "terraform", "ansible", "linux", "git",
    # Data & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "pandas",
    "numpy", "data science", "analytics", "bi", "ai",
    # Tools & Frameworks
    "git", "jira", "confluence", "rest api", "graphql", "grpc", "websocket",
    "oauth", "jwt", "soap", "xml", "json", "yaml",
    # Other
    "agile", "scrum", "microservices", "monolith", "api", "testing", "unit test",
    "integration test", "e2e", "design patterns", "solid", "clean code"
}

def extract_skills_fallback(text: str) -> list:
    """
    Fallback skill extraction using keyword matching when AI is not available
    """
    text_lower = text.lower()
    found_skills = set()
    
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill.title())
    
    return sorted(list(found_skills))

def get_missing_skills_for_goal(goal: str) -> list:
    """
    Get common missing skills recommendations based on goal
    """
    goal_lower = goal.lower()
    recommendations = []
    
    if any(word in goal_lower for word in ["frontend", "web", "ui", "ux"]):
        recommendations = ["React", "TypeScript", "Vue.js", "Responsive Design", "Webpack"]
    elif any(word in goal_lower for word in ["backend", "api", "server"]):
        recommendations = ["PostgreSQL", "RESTful APIs", "Microservices", "Kubernetes"]
    elif any(word in goal_lower for word in ["full stack", "fullstack"]):
        recommendations = ["TypeScript", "Kubernetes", "CI/CD", "Testing"]
    elif any(word in goal_lower for word in ["data", "analytics", "ml", "science"]):
        recommendations = ["Pandas", "Statistics", "Deep Learning", "Spark"]
    elif any(word in goal_lower for word in ["devops", "infra", "cloud"]):
        recommendations = ["Terraform", "Linux", "Ansible", "Monitoring"]
    else:
        recommendations = ["Testing", "Design Patterns", "Documentation"]
    
    return recommendations

def analyze_resume(text: str, goal: str) -> dict:
    """
    Use AI to find:
    - skills present in resume
    - missing skills based on user's goal
    Returns: {"skills": [...], "missing_skills": [...]}
    
    Falls back to keyword matching if AI/Groq is unavailable
    """
    if not text or len(text.strip()) < 30:
        return {"skills": [], "missing_skills": []}

    # Try AI extraction first if client is available
    if client:
        system_prompt = (
            "You are a strict resume analyzer. "
            "Return ONLY valid JSON. No markdown, no extra text."
        )

        user_prompt = f"""
Analyze the following resume text and user goal.

Resume:
{text}

User Goal:
{goal}

Task:
1) List the skills clearly mentioned in the resume.
2) List the important skills missing for the user's goal.

Return JSON exactly like:
{{
  "skills": ["skill1", "skill2"],
  "missing_skills": ["skillA", "skillB"]
}}

Rules:
- Keep each list max 25 items
- No duplicates
- Use short skill names (e.g., "React", "Node.js", "SQL")
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            data = json.loads(content)

            skills = data.get("skills", [])
            missing = data.get("missing_skills", [])

            # Safety + cleanup
            if not isinstance(skills, list): skills = []
            if not isinstance(missing, list): missing = []

            skills = sorted({str(s).strip() for s in skills if str(s).strip()})
            missing = sorted({str(s).strip() for s in missing if str(s).strip()})

            return {"skills": skills, "missing_skills": missing}

        except Exception as e:
            print(f"Warning: AI analysis failed, falling back to keyword extraction: {e}")
    
    # Fallback: keyword-based extraction
    skills = extract_skills_fallback(text)
    missing = get_missing_skills_for_goal(goal)
    
    # Remove skills from missing list if they're already known (case-insensitive)
    skills_lower = {s.lower() for s in skills}
    missing = [s for s in missing if s.lower() not in skills_lower]
    
    return {"skills": skills, "missing_skills": missing}