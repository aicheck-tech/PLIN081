from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from tasks.config import PATH
from tasks.auth import authenticate_user, get_current_user
from tasks.task_helpers import get_user_submissions, save_submission, get_user_annotation_scores
from tasks.models import TaskSubmission, LoginForm

router = APIRouter()
templates = Jinja2Templates(directory=PATH.parent / "templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    username = request.session.get("username")
    if username:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("index.html", {"request": request, "username": username})


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        login_data = LoginForm(username=username, password=password)
        if authenticate_user(login_data.username, login_data.password):
            request.session["username"] = login_data.username
            return RedirectResponse("/dashboard", status_code=302)
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    except ValidationError as e:
        error_messages = [error["msg"] for error in e.errors()]
        return templates.TemplateResponse("login.html", {"request": request, "error": "; ".join(error_messages)})


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = Depends(get_current_user)):
    submissions = get_user_submissions(username)
    has_submissions = any(len(submissions[k]) > 0 for k in submissions)
    stats = {
        "total": sum(len(submissions[k]) for k in submissions),
        "story": len(submissions["story"]),
        "theme": len(submissions["theme"]),
        "education": len(submissions["education"]),
        "questions": len(submissions["questions"])
    }
    annotation_scores = get_user_annotation_scores(username)   # <--- add this line
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": username,
            "has_submissions": has_submissions,
            "story_submissions": submissions["story"],
            "theme_submissions": submissions["theme"],
            "education_submissions": submissions["education"],
            "questions_submissions": submissions["questions"],
            "stats": stats,
            "annotation_scores": annotation_scores,   # <--- add this line
        },
    )

@router.get("/submit", response_class=HTMLResponse)
async def submission_form(
    request: Request,
    username: str = Depends(get_current_user),
    category: Optional[str] = Query(None),
    id: Optional[int] = Query(None)
):
    """
    Show new submission form or prefill for editing.
    If 'id' and 'category' are provided, pre-fill the corresponding submission for edit.
    """
    user_data = {}
    editing = False
    editing_category = None

    if category and id:
        # Find the specific submission to edit
        submissions = get_user_submissions(username)
        for item in submissions.get(category, []):
            if str(item.get("id")) == str(id):
                user_data = item
                editing = True
                editing_category = category  # Set category for template
                break

    return templates.TemplateResponse(
        "submit_form.html",
        {
            "request": request,
            "username": username,
            "editing": editing,
            "editing_category": editing_category,   # <-- pass this to template
            "user_data": user_data,
        },
    )


@router.post("/submit")
async def submit_task(
    request: Request,
    categories: list[str] = Form(...),  # Accept multiple categories
    id: Optional[int] = Form(None),
    prompt: Optional[str] = Form(""),
    technology: Optional[str] = Form(""),
    story: Optional[str] = Form(""),
    theme_prompt: Optional[str] = Form(""),
    theme_placeholders: Optional[str] = Form(""),
    theme_story: Optional[str] = Form(""),
    theme_original_story: Optional[str] = Form(""),
    education_prompt: Optional[str] = Form(""),
    education_placeholders: Optional[str] = Form(""),
    education_story: Optional[str] = Form(""),
    education_original_story: Optional[str] = Form(""),
    questions_prompt: Optional[str] = Form(""),
    questions_placeholders: Optional[str] = Form(""),
    questions: Optional[str] = Form(""),
    questions_original_story: Optional[str] = Form(""),
    username: str = Depends(get_current_user),
):
    """
    Handle submission POST for unlimited submissions per set of categories.
    At least one filled section should be posted; all filled sections will be saved.
    """
    try:
        data = {
            "prompt": prompt,
            "technology": technology,
            "story": story,
            "theme_prompt": theme_prompt,
            "theme_placeholders": theme_placeholders,
            "theme_story": theme_story,
            "theme_original_story": theme_original_story,
            "education_prompt": education_prompt,
            "education_placeholders": education_placeholders,
            "education_story": education_story,
            "education_original_story": education_original_story,
            "questions_prompt": questions_prompt,
            "questions_placeholders": questions_placeholders,
            "questions": questions,
            "questions_original_story": questions_original_story,
        }

        # Validate all categories requested
        for category in categories:
            if category == "story":
                TaskSubmission(
                    prompt=prompt, technology=technology, story=story
                )
            elif category == "theme":
                TaskSubmission(
                    theme_prompt=theme_prompt,
                    theme_placeholders=theme_placeholders,
                    theme_story=theme_story,
                    theme_original_story=theme_original_story,
                    technology=technology
                )
            elif category == "education":
                TaskSubmission(
                    education_prompt=education_prompt,
                    education_placeholders=education_placeholders,
                    education_story=education_story,
                    education_original_story=education_original_story,
                    technology=technology
                )
            elif category == "questions":
                TaskSubmission(
                    questions_prompt=questions_prompt,
                    questions=questions,
                    questions_placeholders=questions_placeholders,
                    questions_original_story=questions_original_story,
                    technology=technology
                )
            else:
                raise ValidationError([{"msg": f"Invalid category: {category}"}], TaskSubmission)

        success = save_submission(username, data, categories, submission_id=id)
        if success:
            return RedirectResponse(url="/dashboard", status_code=302)

        return templates.TemplateResponse(
            "submit_form.html",
            {
                "request": request,
                "username": username,
                "user_data": data,
                "error": "Failed to save submission",
                "editing": id is not None,
            },
        )
    except ValidationError as e:
        error_messages = [error["msg"] for error in e.errors()]
        return templates.TemplateResponse(
            "submit_form.html",
            {
                "request": request,
                "username": username,
                "user_data": data,
                "error": "; ".join(error_messages),
                "editing": id is not None,
            },
        )

