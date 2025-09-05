import random
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from tasks.config import PATH
from tasks.auth import get_current_user
from tasks.annotation_helpers import (
    get_all_submissions,
    get_annotations_for_submission,
    already_annotated_by,
    save_annotation, get_user_annotations
)

router = APIRouter()
templates = Jinja2Templates(directory=PATH.parent / "templates")

@router.get("/annotate", response_class=HTMLResponse)
async def annotate_form(
    request: Request,
    username: str = Depends(get_current_user),
    category: Optional[str] = Query(None)
):
    item = None
    if category:
        # Find eligible submissions: not by user, 0/1/2 annotations, not already annotated by user
        all_subs = get_all_submissions(category)
        eligible = []
        for s in all_subs:
            if str(s.get("user")) == username:
                continue
            annotations = get_annotations_for_submission(int(s["id"]), category)
            if already_annotated_by(int(s["id"]), category, username):
                continue
            if len(annotations) in (0, 1, 2):
                eligible.append(s)
        item = random.choice(eligible) if eligible else None

    return templates.TemplateResponse(
        "annotate.html",
        {
            "request": request,
            "username": username,
            "category": category,
            "item": item
        },
    )

@router.post("/annotate")
async def submit_annotation(
    request: Request,
    username: str = Depends(get_current_user),
    submission_id: int = Form(...),
    category: str = Form(...),
    # Story
    age_appropriateness: Optional[str] = Form(None),
    clarity: Optional[str] = Form(None),
    creativity: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    literature: Optional[str] = Form(None),
    # Theme
    theme_quality: Optional[str] = Form(None),
    theme_success: Optional[str] = Form(None),
    roleplaying: Optional[str] = Form(None),
    # Education
    education_quality: Optional[str] = Form(None),
    naturalness: Optional[str] = Form(None),
    correctness: Optional[str] = Form(None),
    # Questions
    difficulty: Optional[str] = Form(None),
    completeness: Optional[str] = Form(None),
    correctness_of_responses: Optional[str] = Form(None),
    # Notes (all)
    notes: Optional[str] = Form(""),
):
    # Helper: convert checkbox value (None/str) to int 0/1
    def b(val):
        return int(bool(val))

    annotation_fields = {}
    if category == "story":
        annotation_fields = {
            "age_appropriateness": b(age_appropriateness),
            "clarity": b(clarity),
            "creativity": b(creativity),
            "language": b(language),
            "message": b(message),
            "literature": b(literature),
        }
    elif category == "theme":
        annotation_fields = {
            "theme_quality": b(theme_quality),
            "theme_success": b(theme_success),
            "roleplaying": b(roleplaying),
        }
    elif category == "education":
        annotation_fields = {
            "education_quality": b(education_quality),
            "naturalness": b(naturalness),
            "correctness": b(correctness),
        }
    elif category == "questions":
        annotation_fields = {
            "difficulty": b(difficulty),
            "completeness": b(completeness),
            "correctness_of_responses": b(correctness_of_responses),
        }
    annotation_fields["notes"] = notes or ""

    save_annotation(submission_id, category, username, annotation_fields)
    return RedirectResponse("/annotate?category=" + category, status_code=302)


@router.get("/my-annotations", response_class=HTMLResponse)
async def annotate_dashboard(request: Request, username: str = Depends(get_current_user)):
    annotation_stats, all_annotations = get_user_annotations(username)
    return templates.TemplateResponse(
        "annotate_dashboard.html",
        {
            "request": request,
            "username": username,
            "annotation_stats": annotation_stats,
            "all_annotations": all_annotations,
        }
    )
