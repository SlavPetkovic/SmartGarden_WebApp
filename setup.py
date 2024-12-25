import os

# Define the folder structure relative to the current repository
folders = [
    "app",
    "app/routes",
    "app/templates",
    "app/static",
    "app/static/css",
    "app/static/js",
    "app/static/images",
    "tests"
]

# Define the files to create
files = {
    "README.md": "# SmartGarden WebApp\n\nFastAPI application for managing and monitoring the SmartGarden system.",
    ".gitignore": "__pycache__/\n*.db\n.env",
    "app/main.py": 'from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\nasync def home():\n    return {"message": "SmartGarden API is running"}',
    "app/routes/__init__.py": "",
    "app/routes/api.py": 'from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get("/sensors/latest")\nasync def get_latest_data():\n    return {"message": "Sample sensor data"}',
    "app/routes/web.py": 'from fastapi import APIRouter, Request\nfrom fastapi.responses import HTMLResponse\nfrom fastapi.templating import Jinja2Templates\n\nrouter = APIRouter()\ntemplates = Jinja2Templates(directory="app/templates")\n\n@router.get("/", response_class=HTMLResponse)\nasync def render_dashboard(request: Request):\n    return templates.TemplateResponse("index_test.html", {"request": request})',
    "app/templates/index_test.html": """<!DOCTYPE html>
<html>
<head>
    <title>SmartGarden Dashboard</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <h1>SmartGarden Dashboard</h1>
    <p>Welcome to your SmartGarden!</p>
</body>
</html>""",
    "app/static/css/styles.css": "body { font-family: Arial, sans-serif; }",
    "app/static/js/scripts.js": "console.log('SmartGarden Dashboard Loaded');",
    "app/__init__.py": "",
    "tests/test_routes.py": "def test_sample():\n    assert 1 + 1 == 2",
    "app/db.py": "# Database connection and utility functions placeholder",
    "app/sensors.py": "# Sensor reading and GPIO control functions placeholder",
    "requirements.txt": "fastapi\nuvicorn\njinja2"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with default content
for file_path, content in files.items():
    with open(file_path, "w") as file:
        file.write(content)

print("Folder structure for SmartGarden_webApp created successfully.")
