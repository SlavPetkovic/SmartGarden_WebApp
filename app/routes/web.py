from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db import fetch_latest_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the dashboard page."""
    data = fetch_latest_data()
    return templates.TemplateResponse("index.html", {"request": request, "data": data})
