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

def generate_mcqs_fallback(week_number, week_theme, week_project, missing_skills=None):
    """
    Generate 5 MCQs based on the week's project and theme
    """
    missing_skills = missing_skills or []
    
    mcq_templates = {
        "HTML & CSS Foundations": [
            {
                "question": "Which HTML semantic element should be used for the main navigation menu?",
                "options": ["<div>", "<nav>", "<menu>", "<section>"],
                "correct": 1
            },
            {
                "question": "What CSS property centers a div horizontally and vertically?",
                "options": ["float: center", "display: flex with justify-content and align-items", "position: absolute", "text-align: center"],
                "correct": 1
            },
            {
                "question": "Which selector has the highest specificity in CSS?",
                "options": ["Element selector", "Class selector", "ID selector", "Universal selector"],
                "correct": 2
            },
            {
                "question": "What is the purpose of using semantic HTML in a responsive website?",
                "options": ["Improves SEO and accessibility", "Makes CSS simpler", "Reduces file size", "Increases browser compatibility"],
                "correct": 0
            },
            {
                "question": "How do you make an image responsive in CSS?",
                "options": ["width: 100%", "max-width: 100%", "width: auto", "Both A and B"],
                "correct": 3
            }
        ],
        "JavaScript Fundamentals": [
            {
                "question": "What is the difference between 'let' and 'var' in JavaScript?",
                "options": ["No difference", "'let' is block-scoped, 'var' is function-scoped", "'var' is faster", "'let' can be used globally"],
                "correct": 1
            },
            {
                "question": "Which array method returns a new array without modifying the original?",
                "options": ["push()", "map()", "splice()", "shift()"],
                "correct": 1
            },
            {
                "question": "What does 'this' refer to in a regular function?",
                "options": ["The function itself", "The global object (or undefined in strict mode)", "The parent object", "Nothing"],
                "correct": 1
            },
            {
                "question": "How do you handle errors in asynchronous code using async/await?",
                "options": ["Using .catch()", "Using try/catch block", "Using .finally()", "Errors are automatically caught"],
                "correct": 1
            },
            {
                "question": "What is closure in JavaScript?",
                "options": ["End of a program", "A function that has access to outer function variables", "A loop that closes", "Memory cleanup"],
                "correct": 1
            }
        ],
        "React Basics": [
            {
                "question": "What is the main purpose of React hooks?",
                "options": ["To replace class components entirely", "To add state and side effects to functional components", "To improve performance only", "To handle routing"],
                "correct": 1
            },
            {
                "question": "Which hook is used to handle side effects in React?",
                "options": ["useState", "useEffect", "useContext", "useReducer"],
                "correct": 1
            },
            {
                "question": "What happens when you don't provide a dependency array to useEffect?",
                "options": ["Effect runs once", "Effect never runs", "Effect runs after every render", "Effect runs on unmount"],
                "correct": 2
            },
            {
                "question": "How do you pass data from parent to child component in React?",
                "options": ["Using state", "Using props", "Using context", "Using refs"],
                "correct": 1
            },
            {
                "question": "What is virtual DOM in React?",
                "options": ["Fake JavaScript objects", "In-memory representation of real DOM for optimization", "A security feature", "A debugging tool"],
                "correct": 1
            }
        ]
    }

    # Get MCQs for the theme
    theme_lower = week_theme.lower() if week_theme else "General"
    
    mcqs = None
    for key in mcq_templates:
        if key.lower() in theme_lower.lower():
            mcqs = mcq_templates[key]
            break
    
    # Fallback if no specific template found
    if not mcqs:
        mcqs = [
            {
                "question": f"What is a key concept for '{week_theme}'?",
                "options": ["Understanding fundamentals", "Hands-on practice", "Building projects", "Community learning"],
                "correct": 2
            },
            {
                "question": f"Which skill is most important for '{week_theme}'?",
                "options": ["Reading documentation", "Practical implementation", "Memorization", "Speed"],
                "correct": 1
            },
            {
                "question": f"How should you approach '{week_project}'?",
                "options": ["Copy-paste code", "Build from scratch", "Use templates", "Watch tutorials only"],
                "correct": 1
            },
            {
                "question": f"What is the best way to learn '{week_theme}'?",
                "options": ["Passive reading", "Active practice and building", "Theory only", "Discussion only"],
                "correct": 1
            },
            {
                "question": f"Why is '{week_project}' useful in your learning journey?",
                "options": ["To waste time", "To apply concepts and build portfolio", "To get certificates", "To impress people"],
                "correct": 1
            }
        ]

    # Format as tasks
    tasks = []
    for idx, mcq in enumerate(mcqs[:5], 1):
        tasks.append({
            "id": idx,
            "title": f"MCQ {idx}: {week_theme}",
            "category": "Knowledge",
            "desc": mcq["question"][:60] + "...",
            "time": "5 mins",
            "status": "Pending",
            "type": "mcq",
            "question": mcq["question"],
            "options": mcq["options"],
            "correct": mcq["correct"]
        })

    return tasks

def generate_mcqs(week_number, week_theme, week_project, missing_skills=None):
    """
    Generate MCQs using AI if available, otherwise use fallback
    """
    if not client:
        print("Using fallback MCQ generation (GROQ API not available)")
        return generate_mcqs_fallback(week_number, week_theme, week_project, missing_skills)

    missing_skills = missing_skills or []
    skills_context = ""
    if missing_skills:
        skills_context = f"\n\nFocus on these missing skills: {', '.join(missing_skills[:3])}"

    prompt = f"""
You are an expert instructor creating daily learning MCQs.

Week {week_number}: {week_theme}
Project: {week_project}{skills_context}

Generate 5 multiple-choice questions (MCQs) for daily practice based on this week's content.

Return ONLY valid JSON in this format:
{{
  "mcqs": [
    {{
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct": 0
    }}
  ]
}}

Rules:
- Each question should have 4 options
- 'correct' is the 0-based index of the correct option
- Questions should be practical and skill-based
- Include mix of conceptual and practical questions
- Do NOT include markdown, explanations, or extra text
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

        data = json.loads(raw_json)
        mcqs = data.get("mcqs", [])

        # Format as tasks
        tasks = []
        for idx, mcq in enumerate(mcqs[:5], 1):
            tasks.append({
                "id": idx,
                "title": f"MCQ {idx}: {week_theme}",
                "category": "Knowledge",
                "desc": mcq["question"][:60] + "...",
                "time": "5 mins",
                "status": "Pending",
                "type": "mcq",
                "question": mcq["question"],
                "options": mcq["options"],
                "correct": mcq["correct"]
            })

        return tasks

    except Exception as e:
        print(f"AI MCQ generation failed: {e}. Using fallback.")
        return generate_mcqs_fallback(week_number, week_theme, week_project, missing_skills)
