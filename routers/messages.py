from fastapi import APIRouter, Query
from database import SessionLocal
from models import Message

router = APIRouter()

@router.post("/messages")
def create_message(text: str = Query(min_length=1, max_length=200)):
    db = SessionLocal()
    message = Message(text=text)
    db.add(message)
    db.commit()
    db.refresh(message)
    db.close()
    return {
        "id": message.id,
        "text": message.text,
        "created_at": message.created_at.isoformat()
    }

@router.get("/messages")
def read_messages():
    db = SessionLocal()
    messages = db.query(Message).order_by(Message.created_at.desc()).all()
    db.close()
    return [
        {"id": m.id, "text": m.text, "created_at": m.created_at.isoformat()}
        for m in messages
    ]