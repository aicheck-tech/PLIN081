import json
import os
import logging
from typing import List, Dict
from datetime import datetime

import pandas as pd
import git

from tasks.annotation_helpers import get_all_submissions, ANNOTATION_CSV
from tasks.config import (
    DATA_DIR, STORY_GENERATOR_CSV, THEME_GENERATOR_CSV,
    EDUCATIVE_CONTENT_CSV, QUESTIONS_GENERATOR_CSV
)

logger = logging.getLogger(__name__)


def init_git_repo():
    """Initialize or return existing Git repository."""
    try:
        return git.Repo(DATA_DIR)
    except git.exc.InvalidGitRepositoryError:
        return git.Repo.init(DATA_DIR)

def commit_changes(username: str, operation: str) -> bool:
    """Commit CSV changes to git."""
    try:
        repo = init_git_repo()
        repo.git.add(".")
        commit_message = f"{operation} by {username} at {datetime.now().isoformat()}"
        repo.git.commit("-m", commit_message)
        return True
    except Exception as exc:
        logger.error(f"Git error: {str(exc)}")
        return False

def get_story_generator_df() -> pd.DataFrame:
    columns = ["id", "prompt", "story", "technology", "user", "created_at"]
    if os.path.exists(STORY_GENERATOR_CSV):
        df = pd.read_csv(STORY_GENERATOR_CSV)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

def get_theme_generator_df() -> pd.DataFrame:
    columns = [
        "id", "prompt", "placeholders", "original_story", "new_story",
        "user", "technology", "theme_original_story", "created_at"
    ]
    if os.path.exists(THEME_GENERATOR_CSV):
        df = pd.read_csv(THEME_GENERATOR_CSV)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

def get_educative_content_df() -> pd.DataFrame:
    columns = [
        "id", "prompt", "placeholders", "original_story", "new_story",
        "user", "technology", "education_original_story", "created_at"
    ]
    if os.path.exists(EDUCATIVE_CONTENT_CSV):
        df = pd.read_csv(EDUCATIVE_CONTENT_CSV)
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

def get_questions_generator_df() -> pd.DataFrame:
    columns = [
        "id", "prompt", "questions_placeholders", "original_story", "questions",
        "user", "technology", "questions_original_story", "created_at"
    ]
    if os.path.exists(QUESTIONS_GENERATOR_CSV):
        df = pd.read_csv(QUESTIONS_GENERATOR_CSV)
        # Add any missing columns
        for col in columns:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=columns)

def _next_id(df: pd.DataFrame) -> int:
    if df.empty or "id" not in df.columns or df["id"].isnull().all():
        return 1
    return int(df["id"].dropna().astype(int).max()) + 1

def save_submission(
    username: str,
    data: dict,
    categories: list[str],
    submission_id: int = None
) -> bool:
    """
    Save or update a submission for the user in the given categories (list of category names).
    Each category: 'story', 'theme', 'education', 'questions'.
    If submission_id is provided, update the matching row for that user and id.
    """
    try:
        now = datetime.now().isoformat()
        for category in categories:
            if category == "story":
                df = get_story_generator_df()
                new_row = {
                    "id": int(submission_id) if submission_id else _next_id(df),
                    "prompt": data.get("prompt", ""),
                    "story": data.get("story", ""),
                    "technology": data.get("technology", ""),
                    "user": username,
                    "created_at": now
                }
                if submission_id and not df.empty:
                    mask = (df["id"] == int(submission_id)) & (df["user"] == username)
                    if mask.any():
                        for k, v in new_row.items():
                            df.loc[mask, k] = v
                    else:
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(STORY_GENERATOR_CSV, index=False)

            elif category == "theme":
                df = get_theme_generator_df()
                new_row = {
                    "id": int(submission_id) if submission_id else _next_id(df),
                    "prompt": data.get("theme_prompt", ""),
                    "placeholders": data.get("theme_placeholders", ""),
                    "original_story": data.get("theme_original_story", ""),
                    "new_story": data.get("theme_story", ""),
                    "user": username,
                    "technology": data.get("technology", ""),
                    "theme_original_story": data.get("theme_original_story", ""),
                    "created_at": now
                }
                if submission_id and not df.empty:
                    mask = (df["id"] == int(submission_id)) & (df["user"] == username)
                    if mask.any():
                        for k, v in new_row.items():
                            df.loc[mask, k] = v
                    else:
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(THEME_GENERATOR_CSV, index=False)

            elif category == "education":
                df = get_educative_content_df()
                new_row = {
                    "id": int(submission_id) if submission_id else _next_id(df),
                    "prompt": data.get("education_prompt", ""),
                    "placeholders": data.get("education_placeholders", ""),
                    "original_story": data.get("education_original_story", ""),
                    "new_story": data.get("education_story", ""),
                    "user": username,
                    "technology": data.get("technology", ""),
                    "education_original_story": data.get("education_original_story", ""),
                    "created_at": now
                }
                if submission_id and not df.empty:
                    mask = (df["id"] == int(submission_id)) & (df["user"] == username)
                    if mask.any():
                        for k, v in new_row.items():
                            df.loc[mask, k] = v
                    else:
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(EDUCATIVE_CONTENT_CSV, index=False)

            elif category == "questions":
                df = get_questions_generator_df()
                new_row = {
                    "id": int(submission_id) if submission_id else _next_id(df),
                    "prompt": data.get("questions_prompt", ""),
                    "questions_placeholders": data.get("questions_placeholders", ""),
                    "original_story": data.get("questions_original_story", ""),
                    "questions": data.get("questions", ""),
                    "user": username,
                    "technology": data.get("technology", ""),
                    "questions_original_story": data.get("questions_original_story", ""),
                    "created_at": now
                }
                if submission_id and not df.empty:
                    mask = (df["id"] == int(submission_id)) & (df["user"] == username)
                    if mask.any():
                        for k, v in new_row.items():
                            df.loc[mask, k] = v
                    else:
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(QUESTIONS_GENERATOR_CSV, index=False)
        #commit_changes(username, f"Added or updated submission ({','.join(categories)})")
        return True
    except Exception as e:
        logger.error("Error saving submission: %s", e)
        return False

def get_user_submissions(username: str) -> Dict[str, List[dict]]:
    """
    Return all submissions for this user, divided by category.
    Keys: 'story', 'theme', 'education', 'questions'
    """
    submissions = {
        "story": [],
        "theme": [],
        "education": [],
        "questions": []
    }

    # Story
    story_df = get_story_generator_df()
    if not story_df.empty:
        for _, row in story_df[story_df["user"] == username].iterrows():
            submissions["story"].append({
                "id": row.get("id", ""),
                "prompt": row.get("prompt", ""),
                "story": row.get("story", ""),
                "technology": row.get("technology", ""),
                "created_at": row.get("created_at", "")
            })

    # Theme
    theme_df = get_theme_generator_df()
    if not theme_df.empty:
        for _, row in theme_df[theme_df["user"] == username].iterrows():
            submissions["theme"].append({
                "id": row.get("id", ""),
                "theme_prompt": row.get("prompt", ""),
                "theme_placeholders": row.get("placeholders", ""),
                "theme_original_story": row.get("theme_original_story", "") or row.get("original_story", ""),
                "theme_story": row.get("new_story", ""),
                "technology": row.get("technology", ""),
                "created_at": row.get("created_at", "")
            })

    # Education
    educative_df = get_educative_content_df()
    if not educative_df.empty:
        for _, row in educative_df[educative_df["user"] == username].iterrows():
            submissions["education"].append({
                "id": row.get("id", ""),
                "education_prompt": row.get("prompt", ""),
                "education_placeholders": row.get("placeholders", ""),
                "education_original_story": row.get("education_original_story", "") or row.get("original_story", ""),
                "education_story": row.get("new_story", ""),
                "technology": row.get("technology", ""),
                "created_at": row.get("created_at", "")
            })

    # Questions
    questions_df = get_questions_generator_df()
    if not questions_df.empty:
        for _, row in questions_df[questions_df["user"] == username].iterrows():
            submissions["questions"].append({
                "id": row.get("id", ""),
                "questions_prompt": row.get("prompt", ""),
                "questions_placeholders": row.get("questions_placeholders", ""),
                "questions_original_story": row.get("questions_original_story", "") or row.get("original_story", ""),
                "questions": row.get("questions", ""),
                "technology": row.get("technology", ""),
                "created_at": row.get("created_at", "")
            })

    return submissions

def get_user_annotation_scores(username: str):
    """
    Returns dict with average annotation score for each category for this user.
    Score = sum of all fields marked 1 in this user's submissions / max possible points
    """
    category_fields = {
        "story": ["age_appropriateness", "clarity", "creativity", "language", "message", "literature"],
        "theme": ["theme_quality", "theme_success", "roleplaying"],
        "education": ["education_quality", "naturalness", "correctness"],
        "questions": ["difficulty", "completeness", "correctness_of_responses"],
    }
    if not ANNOTATION_CSV.is_file():
        return {k: {"score": 0, "max": len(v), "count": 0} for k, v in category_fields.items()}

    df = pd.read_csv(ANNOTATION_CSV)
    result = {}
    for cat, fields in category_fields.items():
        # Find all this user's submissions for this category
        subs = get_all_submissions(cat)
        submission_ids = set(str(s["id"]) for s in subs if s["user"] == username)
        if not submission_ids:
            result[cat] = {"score": 0, "max": 100, "count": 0}
            continue
        # All annotations for user's submissions
        cat_df = df[(df["category"] == cat) & (df["submission_id"].astype(str).isin(submission_ids))]
        total_score = 0
        total_possible = 0
        num_annot = 0
        for _, row in cat_df.iterrows():
            annot = json.loads(row["fields_json"])
            s = sum(int(annot.get(f, 0)) for f in fields)
            total_score += s
            total_possible += len(fields)
            num_annot += 1
        avg = (total_score / total_possible) if total_possible else 0
        result[cat] = {
            "score": round(avg * 100, 1) if num_annot > 0 else 0,  # percent
            "max": 100,
            "count": num_annot
        }
    return result
