from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")


MAX_QUESTIONS = 5


all_questions = [
    "Tell me about one of your favorite projects that you have worked on.",
    "Describe a situation where you had to work with a difficult team member.",
    "How do you prioritize tasks when everything seems urgent?",
    "Tell me about a time you automated a manual process.",
    "Describe a failure you experienced in a project. How did you handle it?",
    "What has been the most challenging problem you have faced and how did you solve it?",
    "Describe a time when your communication skills helped you successfully accomplish a project or task.",
    "Tell me about a stressful situation and how you handled it.",
    "Have you ever faced a difficult decision at work? How did you handle it?.",
    "How do you handle mistakes in a live production environment?"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.get("/", response_class=HTMLResponse)
async def start_session(request: Request):
    session_id = id(request)
    selected = random.sample(all_questions, MAX_QUESTIONS)
    sessions[session_id] = {"questions": selected, "answers": [], "index": 0}
    return RedirectResponse(f"/question/{session_id}")

@app.get("/question/{session_id}", response_class=HTMLResponse)
async def ask_question(request: Request, session_id: int):
    session = sessions.get(session_id)
    if not session or session["index"] >= MAX_QUESTIONS:
        return RedirectResponse(f"/done/{session_id}")

    question = session["questions"][session["index"]]
    question_number = session["index"] + 1
    return templates.TemplateResponse("index.html", {
        "request": request,
        "session_id": session_id,
        "question": question,
        "number": question_number,
        "total": MAX_QUESTIONS
    })

@app.post("/submit", response_class=HTMLResponse)
async def submit_answer(
    request: Request,
    session_id: int = Form(...),
    question: str = Form(...),
    answer: str = Form(...)
):
    session = sessions.get(session_id)
    if session:
        session["answers"].append({"question": question, "answer": answer})
        session["index"] += 1

    if session["index"] >= MAX_QUESTIONS:
        return RedirectResponse(f"/done/{session_id}", status_code=303)
    else:
        return RedirectResponse(f"/question/{session_id}", status_code=303)

@app.get("/done/{session_id}", response_class=HTMLResponse)
async def finish(request: Request, session_id: int):
    return templates.TemplateResponse("done.html", {"request": request})