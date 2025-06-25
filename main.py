from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

questions = [
    "Tell me about a time you handled a production incident.",
    "Describe a situation where you had to work with a difficult team member.",
    "How do you prioritize tasks when everything seems urgent?",
    "Tell me about a time you automated a manual process.",
    "Describe a failure you experienced in a DevOps project. How did you handle it?",
    "Have you ever disagreed with a manager or architect about infrastructure decisions?",
    "How do you ensure clear communication in a remote DevOps team?",
    "Tell me about a stressful situation and how you handled it.",
    "Describe a time when you improved CI/CD pipelines.",
    "How do you handle mistakes in a live production environment?"
]

@app.get("/", response_class=HTMLResponse)
async def read_question(request: Request):
    question = random.choice(questions)
    return templates.TemplateResponse("index.html", {"request": request, "question": question})

@app.post("/submit", response_class=HTMLResponse)
async def submit_answer(request: Request, question: str = Form(...), answer: str = Form(...)):
    # For now, we just print it. You can later save to file or DB.
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    return RedirectResponse("/", status_code=303)