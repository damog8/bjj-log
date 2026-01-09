from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Query

from database import engine, SessionLocal
from models import Base, Message

from routers import messages

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(messages.router)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}, this app is alive on the internet."}

@app.get("/api")
def api_root():
    return {
        "name": "Hello World Messages",
        "status": "ok",
        "endpoints": ["/messages (GET, POST)"]
    }
