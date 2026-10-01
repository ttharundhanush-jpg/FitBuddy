import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.schemas import UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app import database as db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
router = APIRouter()


def _home(request: Request, error: str = ""):
    return templates.TemplateResponse(request, "index.html", {"error": error})


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return _home(request)


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        user = UserInput(username=username.strip(), user_id=user_id, age=age,
                         weight=weight, goal=goal.strip(), intensity=intensity.lower())
    except ValidationError as e:
        msg = "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors())
        return _home(request, msg)

    plan = generate_workout_gemini(user)
    tip = generate_nutrition_tip_with_flash(user.goal)
    db.save_user(user.user_id, user.username, user.age, user.weight, user.goal, user.intensity)
    db.save_plan(user.user_id, plan, tip)

    return templates.TemplateResponse(request, "result.html", {
        "username": user.username, "user_id": user.user_id, "age": user.age,
        "weight": user.weight, "goal": user.goal, "intensity": user.intensity,
        "workout_plan": plan, "updated_plan": None, "nutrition_tip": tip,
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: int = Form(...), feedback: str = Form(...)):
    try:
        fb = FeedbackRequest(user_id=user_id, feedback=feedback.strip())
    except ValidationError:
        return _home(request, "Feedback must be at least 2 characters.")

    user, plan = db.get_user(fb.user_id), db.get_plan(fb.user_id)
    if not user or not plan:
        return _home(request, f"No plan found for user ID {fb.user_id}. Generate one first.")

    base = plan.updated_plan or plan.original_plan
    updated = update_workout_plan(base, fb.feedback)
    db.update_plan(fb.user_id, updated)

    return templates.TemplateResponse(request, "result.html", {
        "username": user.name, "user_id": user.id, "age": user.age,
        "weight": user.weight, "goal": user.goal, "intensity": user.intensity,
        "workout_plan": plan.original_plan, "updated_plan": updated,
        "nutrition_tip": plan.nutrition_tip,
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    plans = {p.user_id: p for p in db.get_all_plans()}
    data = []
    for u in db.get_all_users():
        p = plans.get(u.id)
        data.append({
            "id": u.id, "name": u.name, "age": u.age, "weight": u.weight,
            "goal": u.goal, "intensity": u.intensity,
            "original_plan": p.original_plan if p else "N/A",
            "updated_plan": p.updated_plan if p and p.updated_plan else "Not updated",
        })
    return templates.TemplateResponse(request, "all_users.html", {"users": data})
