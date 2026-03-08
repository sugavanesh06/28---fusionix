import os
import json
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

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def generate_roadmap_fallback(goal, skills, missing_skills):
    """
    Generate a fixed 8-week actionable roadmap with themes, build tasks, and capstone projects
    """
    skills_list = [s.strip() for s in skills if s.strip()] if isinstance(skills, list) else []
    missing_list = [s.strip() for s in missing_skills if s.strip()] if isinstance(missing_skills, list) else []

    # Define 8-week themes based on common career paths
    week_themes = {
        "frontend": [
            "HTML & CSS Foundations",
            "JavaScript Fundamentals",
            "React Basics",
            "Advanced React",
            "State Management",
            "API Integration",
            "Testing & Debugging",
            "Deployment & Optimization"
        ],
        "backend": [
            "Programming Fundamentals",
            "Database Design",
            "API Development",
            "Authentication & Security",
            "Server Architecture",
            "Microservices",
            "Testing & Monitoring",
            "Deployment & Scaling"
        ],
        "fullstack": [
            "Web Foundations",
            "JavaScript Mastery",
            "Frontend Frameworks",
            "Backend Development",
            "Database Integration",
            "Full-Stack Projects",
            "Testing & DevOps",
            "Production Deployment"
        ],
        "data": [
            "Python Programming",
            "Data Analysis",
            "SQL Databases",
            "Data Visualization",
            "Machine Learning",
            "Big Data Tools",
            "Data Engineering",
            "AI/ML Projects"
        ],
        "devops": [
            "Linux & Shell Scripting",
            "Version Control",
            "CI/CD Pipelines",
            "Containerization",
            "Cloud Platforms",
            "Infrastructure as Code",
            "Monitoring & Logging",
            "Site Reliability"
        ]
    }

    # Determine career path from goal
    goal_lower = goal.lower() if goal else ""
    if "frontend" in goal_lower or "ui" in goal_lower or "ux" in goal_lower:
        themes = week_themes["frontend"]
    elif "backend" in goal_lower or "server" in goal_lower or "api" in goal_lower:
        themes = week_themes["backend"]
    elif "full" in goal_lower and "stack" in goal_lower:
        themes = week_themes["fullstack"]
    elif "data" in goal_lower or "analyst" in goal_lower or "scientist" in goal_lower:
        themes = week_themes["data"]
    elif "devops" in goal_lower or "infrastructure" in goal_lower or "cloud" in goal_lower:
        themes = week_themes["devops"]
    else:
        # Default to fullstack if goal not recognized
        themes = week_themes["fullstack"]

    # Map missing skills to appropriate weeks
    skill_assignments = {}
    for i, skill in enumerate(missing_list):
        week_num = min(i + 1, 8)  # Assign to weeks 1-8
        if f"week{week_num}" not in skill_assignments:
            skill_assignments[f"week{week_num}"] = []
        skill_assignments[f"week{week_num}"].append(skill)

    quick_start = {
        "days": "3-5",
        "description": f"Launch your {goal} journey with hands-on setup",
        "tasks": [
            "Set up your development environment and tools",
            "Create your first 'Hello World' application",
            "Build a simple portfolio landing page",
            "Set up version control and deployment basics"
        ]
    }

    detailed_roadmap = {}

    # Generate exactly 8 weeks
    for week in range(1, 9):
        theme = themes[week - 1] if week <= len(themes) else f"Advanced {goal} Concepts"
        week_skills = skill_assignments.get(f"week{week}", [])

        # Create actionable build tasks based on theme
        tasks = generate_actionable_tasks(theme, week_skills, goal)

        # Create portfolio-ready capstone project
        capstone = generate_capstone_project(theme, week, goal)

        detailed_roadmap[f"week{week}"] = {
            "week": week,
            "focus": theme,
            "skills": week_skills if week_skills else [theme.split()[0]],  # Fallback to first word of theme
            "tasks": tasks,
            "mini_project": capstone
        }

    return {
        "quick_start": quick_start,
        "detailed_roadmap": detailed_roadmap,
        "summary": f"8-week intensive roadmap to become a {goal} with portfolio-ready projects each week"
    }

def generate_actionable_tasks(theme, skills, goal):
    """Generate actionable build tasks instead of passive learning"""
    task_templates = {
        "HTML & CSS Foundations": [
            "Build a responsive personal portfolio website from scratch",
            "Create a multi-page business website with navigation",
            "Develop a product landing page with call-to-action sections",
            "Implement responsive layouts for mobile and desktop"
        ],
        "JavaScript Fundamentals": [
            "Build an interactive calculator with multiple operations",
            "Create a dynamic to-do list application with local storage",
            "Develop a weather app that fetches real-time data",
            "Implement form validation with custom error messages"
        ],
        "React Basics": [
            "Build a React component library with reusable UI elements",
            "Create a task management app with add/edit/delete functionality",
            "Develop a photo gallery with filtering and search",
            "Implement a multi-step form wizard with progress tracking"
        ],
        "Advanced React": [
            "Build a full e-commerce product catalog with cart",
            "Create a social media dashboard with data visualization",
            "Develop a real-time chat application with WebSocket",
            "Implement a complex form with dynamic field generation"
        ],
        "State Management": [
            "Build a Redux store for a complex application state",
            "Create a context API system for theme switching",
            "Develop a custom hooks library for common functionality",
            "Implement state persistence across browser sessions"
        ],
        "API Integration": [
            "Build a RESTful API client with authentication",
            "Create a GraphQL client for data fetching",
            "Develop a third-party API integration (GitHub, Twitter)",
            "Implement error handling and loading states for API calls"
        ],
        "Testing & Debugging": [
            "Write comprehensive unit tests for React components",
            "Create integration tests for user workflows",
            "Develop end-to-end tests with Cypress",
            "Build debugging tools and error boundary components"
        ],
        "Deployment & Optimization": [
            "Deploy a React app to Vercel/Netlify with CI/CD",
            "Implement performance optimizations and lazy loading",
            "Set up monitoring and error tracking",
            "Create a production build with code splitting"
        ],
        "Programming Fundamentals": [
            "Build a command-line task manager in Python",
            "Create algorithms for sorting and searching data",
            "Develop a file processing utility with error handling",
            "Implement data structures (stacks, queues, trees)"
        ],
        "Database Design": [
            "Design and implement a relational database schema",
            "Build a database migration system",
            "Create optimized queries with indexing",
            "Develop a database backup and restore utility"
        ],
        "API Development": [
            "Build a REST API with CRUD operations",
            "Create API documentation with Swagger/OpenAPI",
            "Implement rate limiting and request validation",
            "Develop API versioning and backward compatibility"
        ],
        "Authentication & Security": [
            "Implement JWT-based authentication system",
            "Create role-based access control (RBAC)",
            "Build secure password hashing and validation",
            "Develop API security with CORS and helmet"
        ],
        "Server Architecture": [
            "Design a scalable microservices architecture",
            "Build a load balancer with Nginx",
            "Create a caching layer with Redis",
            "Implement message queues for async processing"
        ],
        "Microservices": [
            "Build a microservices communication system",
            "Create service discovery and registration",
            "Develop distributed tracing and logging",
            "Implement circuit breakers and retry logic"
        ],
        "Testing & Monitoring": [
            "Write comprehensive API tests with pytest",
            "Create monitoring dashboards with Grafana",
            "Build health check endpoints",
            "Implement logging and error tracking"
        ],
        "Deployment & Scaling": [
            "Deploy to AWS/GCP with infrastructure as code",
            "Set up auto-scaling and load balancing",
            "Create CI/CD pipelines with GitHub Actions",
            "Implement blue-green deployment strategy"
        ]
    }

    # Get tasks for the theme, or use generic build tasks
    if theme in task_templates:
        return task_templates[theme]
    else:
        # Generic actionable tasks for unrecognized themes
        return [
            f"Build a practical application demonstrating {theme}",
            f"Create a library or utility for {theme} functionality",
            f"Develop a tutorial project teaching {theme} concepts",
            f"Implement a real-world use case for {theme}"
        ]

def generate_capstone_project(theme, week, goal):
    """Generate portfolio-ready capstone projects for each week"""
    capstone_projects = {
        "HTML & CSS Foundations": "Complete responsive portfolio website with contact form and project showcase",
        "JavaScript Fundamentals": "Interactive web application with dynamic content and user interactions",
        "React Basics": "Full-featured React application with routing and state management",
        "Advanced React": "Complex React application with advanced patterns and optimizations",
        "State Management": "Scalable application with complex state logic and data flow",
        "API Integration": "Full-stack application with backend API and frontend client",
        "Testing & Debugging": "Production-ready application with comprehensive test coverage",
        "Deployment & Optimization": "Optimized, deployed application with monitoring and analytics",
        "Programming Fundamentals": "Command-line application solving real-world problems",
        "Database Design": "Data-driven application with complex database operations",
        "API Development": "RESTful API serving multiple client applications",
        "Authentication & Security": "Secure web application with user authentication and authorization",
        "Server Architecture": "Scalable server application handling high traffic loads",
        "Microservices": "Microservices architecture with multiple communicating services",
        "Testing & Monitoring": "Monitored application with comprehensive testing and observability",
        "Deployment & Scaling": "Cloud-deployed application with auto-scaling capabilities"
    }

    if theme in capstone_projects:
        return capstone_projects[theme]
    else:
        return f"Portfolio-ready {goal} project demonstrating {theme} mastery"

def generate_roadmap(goal, skills, missing_skills):
    """
    Generate roadmap using AI if available, otherwise use fallback
    """
    if not client:
        print("Using fallback roadmap generation (GROQ API not available)")
        return generate_roadmap_fallback(goal, skills, missing_skills)
    
    prompt = f"""
You are a career mentor.

Goal: {goal}

Current Skills:
{skills}

Missing Skills:
{missing_skills}

Create:
1) Quick Start Plan (3-5 days)
2) Detailed Roadmap (maximum 8 weeks)

Each week must include:
- focus
- skills
- tasks
- mini_project

Return JSON format:
{{
  "quick_start": {{}},
  "detailed_roadmap": {{}}
}}

IMPORTANT:
- Return ONLY valid JSON.
- Do NOT include markdown, headings, code fences, or explanations.
- Output must start with {{ and end with }}.
- If you include "days", it must be a STRING like "3-5", not 3-5.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content.strip()

        start = raw.find("{")
        end = raw.rfind("}")
        raw_json = raw[start:end+1]

        roadmap_dict = json.loads(raw_json)
        return roadmap_dict
    except Exception as e:
        print(f"AI roadmap generation failed: {e}. Using fallback.")
        return generate_roadmap_fallback(goal, skills, missing_skills)