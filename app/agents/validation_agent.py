from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def validate_task(task_title, task_description, submission_text):
    prompt = f"""
You are evaluating a user's submitted task.

Task Title: {task_title}
Task Description: {task_description}
User Submission: {submission_text}

Return ONLY valid JSON:
{{
  "score": "8/10",
  "feedback": "",
  "status": "approved"
}}

Rules:
- score should be simple like 7/10
- feedback should be short and practical
- status should be approved or needs_improvement
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    return json.loads(raw[start:end+1])