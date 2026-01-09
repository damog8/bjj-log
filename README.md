# BJJ Training Log

A tiny full-stack app built with **FastAPI + SQLite**, featuring a minimal HTML UI to create and view timestamped messages.

This project was built as part of a 2026 builder practice to learn how to:
- design APIs
- persist data
- serve a UI
- deploy a real app
- debug end-to-end

---

## Features
- Create messages (POST `/messages`)
- View messages (GET `/messages`)
- Validation (max 200 characters)
- Timestamps (UTC)
- Minimal HTML UI
- Deployed to Render

---

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- Vanilla HTML + JS

---

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
