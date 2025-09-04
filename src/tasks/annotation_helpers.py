import os
import json
from datetime import datetime
import pandas as pd

from tasks.config import (
    DATA_DIR, STORY_GENERATOR_CSV, THEME_GENERATOR_CSV,
    EDUCATIVE_CONTENT_CSV, QUESTIONS_GENERATOR_CSV
)

ANNOTATION_CSV = DATA_DIR / "annotations.csv"

def _next_annotation_id(df: pd.DataFrame) -> int:
    if df.empty or "id" not in df.columns or df["id"].isnull().all():
        return 1
    return int(df["id"].dropna().astype(int).max()) + 1

def save_annotation(submission_id: int, category: str, username: str, fields: dict):
    """Save a new annotation (always new, never update)."""
    now = datetime.now().isoformat()
    df = pd.read_csv(ANNOTATION_CSV) if os.path.exists(ANNOTATION_CSV) else pd.DataFrame(columns=[
        "id", "submission_id", "category", "fields_json", "user", "created_at"
    ])
    new_row = {
        "id": _next_annotation_id(df),
        "submission_id": submission_id,
        "category": category,
        "fields_json": json.dumps(fields),
        "user": username,
        "created_at": now,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(ANNOTATION_CSV, index=False)

def get_annotations_for_submission(submission_id: int, category: str):
    """Return all annotations for a submission (list of dicts)."""
    if not os.path.exists(ANNOTATION_CSV):
        return []
    df = pd.read_csv(ANNOTATION_CSV)
    return [
        json.loads(row["fields_json"])
        for _, row in df[
            (df["submission_id"] == submission_id) & (df["category"] == category)
        ].iterrows()
    ]

def already_annotated_by(submission_id: int, category: str, username: str) -> bool:
    if not os.path.exists(ANNOTATION_CSV):
        return False
    df = pd.read_csv(ANNOTATION_CSV)
    mask = (
        (df["submission_id"] == submission_id) &
        (df["category"] == category) &
        (df["user"] == username)
    )
    return mask.any()

def get_all_submissions(category: str):
    """Return a list of all submissions for the given category from all users, with all needed fields."""
    if category == "story":
        csv_file = STORY_GENERATOR_CSV
        fields = ["id", "user", "technology", "prompt", "story"]
    elif category == "theme":
        csv_file = THEME_GENERATOR_CSV
        fields = [
            "id", "user", "technology",
            "prompt",                # Theme prompt
            "placeholders",          # Theme placeholders
            "new_story",             # Theme result
            "theme_original_story",  # Theme original
            "original_story"         # For backward compatibility
        ]
    elif category == "education":
        csv_file = EDUCATIVE_CONTENT_CSV
        fields = [
            "id", "user", "technology",
            "prompt",                  # Education prompt
            "placeholders",            # Education placeholders
            "new_story",               # Education story
            "education_original_story",# Education original
            "original_story"           # For backward compatibility
        ]
    elif category == "questions":
        csv_file = QUESTIONS_GENERATOR_CSV
        fields = [
            "id", "user", "technology",
            "prompt",                  # Questions prompt
            "questions",               # Questions
            "questions_original_story",# Questions original
            "original_story"           # For backward compatibility
        ]
    else:
        return []

    if not os.path.exists(csv_file):
        return []
    df = pd.read_csv(csv_file)
    result = []
    for _, row in df.iterrows():
        d = {k: row[k] if k in row and pd.notnull(row[k]) else "" for k in fields}
        # Normalize to template field names (Jinja expects user_data.theme_prompt, not user_data.prompt etc.)
        if category == "theme":
            d["theme_prompt"] = d.get("prompt", "")
            d["theme_placeholders"] = d.get("placeholders", "")
            d["theme_story"] = d.get("new_story", "")
            d["theme_original_story"] = d.get("theme_original_story", "") or d.get("original_story", "")
        if category == "education":
            d["education_prompt"] = d.get("prompt", "")
            d["education_placeholders"] = d.get("placeholders", "")
            d["education_story"] = d.get("new_story", "")
            d["education_original_story"] = d.get("education_original_story", "") or d.get("original_story", "")
        if category == "questions":
            d["questions_prompt"] = d.get("prompt", "")
            d["questions"] = d.get("questions", "")
            d["questions_original_story"] = d.get("questions_original_story", "") or d.get("original_story", "")
        result.append(d)
    return result
