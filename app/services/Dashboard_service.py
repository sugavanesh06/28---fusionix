from datetime import datetime
from app.models.interview_session import InterviewSession
from app.agents.interview_agent import (
    generate_first_question,
    generate_followup_question,
    evaluate_answer
)

INTERVIEW_DURATION_SECONDS = 120
MAX_QUESTIONS = 3

def start_interview(db, user_id, role):
    # close previous active sessions
    old_sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == user_id,
        InterviewSession.status == "active"
    ).all()

    for old in old_sessions:
        old.status = "completed"

    first_question = generate_first_question(role)

    session = InterviewSession(
        user_id=user_id,
        role=role,
        current_question=first_question,
        question_count=1,
        total_score=0,
        status="active"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "question": first_question,
        "question_number": 1,
        "time_limit_seconds": INTERVIEW_DURATION_SECONDS
    }

def answer_interview(db, session_id, answer):
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()

    if not session:
        return {"error": "Interview session not found"}

    if session.status != "active":
        return {"error": "Interview already completed"}

    elapsed = (datetime.utcnow() - session.started_at).total_seconds()

    result = evaluate_answer(session.current_question, answer)
    score = result.get("score", 0)
    feedback = result.get("feedback", "")

    session.total_score += score

    # Stop interview if time over or max questions reached
    if elapsed >= INTERVIEW_DURATION_SECONDS or session.question_count >= MAX_QUESTIONS:
        session.status = "completed"
        db.commit()

        avg_score = round(session.total_score / session.question_count, 1)

        strengths = []
        weaknesses = []
        recommended_skills = []

        if avg_score >= 8:
            strengths = ["Strong conceptual understanding", "Good interview readiness"]
            weaknesses = ["Can improve answer depth with examples"]
            recommended_skills = ["Advanced problem solving", "System design basics"]
        elif avg_score >= 6:
            strengths = ["Basic understanding is good"]
            weaknesses = ["Needs more technical depth and clarity"]
            recommended_skills = ["Core concepts revision", "Practical implementation", "Mock interview practice"]
        else:
            strengths = ["Willingness to answer and attempt"]
            weaknesses = ["Needs better understanding of core concepts"]
            recommended_skills = ["Concept revision", "Hands-on tasks", "Project practice"]

        return {
            "status": "completed",
            "score": score,
            "feedback": feedback,
            "final_average_score": avg_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_skills": recommended_skills,
            "message": "Interview completed"
        }

    # Generate follow-up question
    next_question = generate_followup_question(
        session.role,
        session.current_question,
        answer
    )

    session.current_question = next_question
    session.question_count += 1
    db.commit()

    return {
        "status": "active",
        "score": score,
        "feedback": feedback,
        "next_question": next_question,
        "question_number": session.question_count
    }