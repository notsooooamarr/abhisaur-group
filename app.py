from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json, os, datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

LEADS_FILE = "data/leads.json"
os.makedirs("data", exist_ok=True)
if not os.path.exists(LEADS_FILE):
    with open(LEADS_FILE, "w") as f:
        json.dump([], f)

def save_lead(data: dict):
    with open(LEADS_FILE, "r") as f:
        leads = json.load(f)
    leads.append(data)
    with open(LEADS_FILE, "w") as f:
        json.dump(leads, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    return templates.TemplateResponse(request, "services.html")

@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return templates.TemplateResponse(request, "projects.html")

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html")

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    return templates.TemplateResponse(request, "contact.html")

@app.post("/api/contact")
async def submit_contact(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(""),
    service: str = Form(...),
    message: str = Form("")
):
    lead = {
        "name": name,
        "phone": phone,
        "email": email,
        "service": service,
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()
    }
    save_lead(lead)
    return JSONResponse({"status": "success", "message": "We'll contact you within 24 hours!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
