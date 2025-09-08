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
            "prompt",                     # Questions prompt
            "questions_placeholders",     # New field
            "questions",                  # Questions+responses
            "questions_original_story",   # Questions original
            "original_story"              # For backward compatibility
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
            d["questions_placeholders"] = d.get("questions_placeholders", "")
            d["questions"] = d.get("questions", "")
            d["questions_original_story"] = d.get("questions_original_story", "") or d.get("original_story", "")
        result.append(d)
    return result
import os
import json
import pandas as pd

from tasks.config import (
    DATA_DIR, STORY_GENERATOR_CSV, THEME_GENERATOR_CSV,
    EDUCATIVE_CONTENT_CSV, QUESTIONS_GENERATOR_CSV
)
from tasks.annotation_helpers import get_all_submissions

ANNOTATION_CSV = DATA_DIR / "annotations.csv"


def get_user_annotations(username: str):
    """
    Returns annotation stats and all annotation details for a user.
    Args:
        username: Annotator username.
    Returns:
        (annotation_stats, all_annotations)
        - annotation_stats: dict, per-category count and avg score.
        - all_annotations: list of dicts, all annotations with checked/max_fields,
          plus 'submission_json' for viewing the original submission.
    """
    category_fields = {
        "story": ["age_appropriateness", "clarity", "creativity", "language", "message", "literature"],
        "theme": ["theme_quality", "theme_success", "roleplaying"],
        "education": ["education_quality", "naturalness", "correctness"],
        "questions": ["difficulty", "completeness", "correctness_of_responses"],
    }
    if not os.path.exists(ANNOTATION_CSV):
        stats = {cat: {"count": 0, "avg_score": 0} for cat in category_fields}
        stats["total"] = 0
        return stats, []

    df = pd.read_csv(ANNOTATION_CSV)
    user_df = df[df["user"] == username]
    stats = {}
    total = 0

    for cat, fields in category_fields.items():
        cat_df = user_df[user_df["category"] == cat]
        count = len(cat_df)
        avg = 0
        if count > 0:
            scores = []
            for _, row in cat_df.iterrows():
                try:
                    d = json.loads(row["fields_json"])
                    s = sum(int(d.get(f, 0)) for f in fields)
                    scores.append(100 * s // len(fields) if fields else 0)
                except Exception:
                    continue
            avg = round(sum(scores) / len(scores), 1) if scores else 0
        stats[cat] = {"count": count, "avg_score": avg}
        total += count
    stats["total"] = total

    # All annotations, newest first, with checked/max_fields for the table, plus submission_json
    user_df = user_df.sort_values("created_at", ascending=False)
    all_annotations = []
    for _, row in user_df.iterrows():
        fields_dict = {}
        try:
            fields_dict = json.loads(row["fields_json"])
        except Exception:
            pass
        cat = row["category"]
        cat_fields = category_fields.get(cat, [])
        checked = sum(int(fields_dict.get(f, 0)) for f in cat_fields)
        # Attach the original submission for modal viewing
        submission = {}
        try:
            all_subs = get_all_submissions(cat)
            for sub in all_subs:
                if str(sub["id"]) == str(row["submission_id"]):
                    submission = sub
                    break
        except Exception:
            pass
        ann = {
            "created_at": row["created_at"],
            "category": cat,
            "submission_id": row["submission_id"],
            "fields": fields_dict,
            "checked": checked,
            "max_fields": len(cat_fields),
            "submission_json": submission,  # For modal
        }
        all_annotations.append(ann)
    return stats, all_annotations

