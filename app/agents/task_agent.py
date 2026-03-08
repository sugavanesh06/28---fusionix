from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

def generate_daily_tasks(goal, week, week_data):
    prompt = f"""
You are a career mentor.

Goal: {goal}
Week: {week}

Week roadmap data:
{json.dumps(week_data, indent=2)}

Create 5 daily tasks for this week.

Return ONLY valid JSON in this format:
{{
  "tasks": [
    {{
      "task_title": "",
      "task_description": "",
      "skill": ""
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    start = raw.find("{")
    end = raw.rfind("}")
    raw_json = raw[start:end+1]

    return json.loads(raw_json)