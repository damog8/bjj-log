from sqlalchemy import Column, Integer, String, DateTime, Date
from database import Base
from datetime import datetime, date

class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)

    session_date = Column(Date, default=date.today, index=True)
    focus = Column(String, index=True)
    notes = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
