from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Query

from database import engine, SessionLocal
from models import Base

from routers import logs

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(logs.router)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
def api_root():
    return {
        "name": "BJJ Training Log",
        "status": "ok",
        "endpoints": ["/messages (GET, POST)"]
    }
