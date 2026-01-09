from fastapi import APIRouter, Query
from database import SessionLocal
from models import TrainingLog
from typing import Optional

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
