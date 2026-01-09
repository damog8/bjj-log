from fastapi import APIRouter, Query
from database import SessionLocal
from models import TrainingLog
from typing import Optional
from datetime import date, timedelta
from sqlalchemy import func

router = APIRouter()

@router.post("/logs")
def create_log(
    focus: str = Query(min_length=1, max_length=50),
    notes: str = Query(min_length=1, max_length=500),
    session_date: Optional[str] = None,  # YYYY-MM-DD
):
    db = SessionLocal()

    log = TrainingLog(
        focus=focus,
        notes=notes,
    )

    # Optional date override (simple approach for now)
    if session_date:
        from datetime import date
        log.session_date = date.fromisoformat(session_date)

    db.add(log)
    db.commit()
    db.refresh(log)
    db.close()

    return {
        "id": log.id,
        "session_date": log.session_date.isoformat(),
        "focus": log.focus,
        "notes": log.notes,
        "created_at": log.created_at.isoformat(),
    }

@router.get("/logs")
def read_logs():
    db = SessionLocal()
    logs = (
        db.query(TrainingLog)
        .order_by(TrainingLog.session_date.desc(), TrainingLog.created_at.desc())
        .all()
    )
    db.close()

    return [
        {
            "id": l.id,
            "session_date": l.session_date.isoformat(),
            "focus": l.focus,
            "notes": l.notes,
            "created_at": l.created_at.isoformat(),
        }
        for l in logs
    ]

@router.get("/summary/week")
def weekly_summary():
    today = date.today()

    # Monday = 0, Sunday = 6
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    db = SessionLocal()

    logs = (
        db.query(TrainingLog)
        .filter(
            TrainingLog.session_date >= start_of_week,
            TrainingLog.session_date <= end_of_week,
        )
        .all()
    )

    total_sessions = len(logs)

    # Count sessions by focus
    focus_counts = (
        db.query(
            TrainingLog.focus,
            func.count(TrainingLog.id)
        )
        .filter(
            TrainingLog.session_date >= start_of_week,
            TrainingLog.session_date <= end_of_week,
        )
        .group_by(TrainingLog.focus)
        .all()
    )

    db.close()

    return {
        "week_start": start_of_week.isoformat(),
        "week_end": end_of_week.isoformat(),
        "total_sessions": total_sessions,
        "by_focus": {focus: count for focus, count in focus_counts},
    }
