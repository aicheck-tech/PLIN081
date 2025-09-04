from pathlib import Path

PATH = Path(__file__).parent
DATA_DIR = PATH.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

STORY_GENERATOR_CSV = DATA_DIR / "story_generator.csv"
THEME_GENERATOR_CSV = DATA_DIR / "theme_generator.csv"
EDUCATIVE_CONTENT_CSV = DATA_DIR / "educative_content_generator.csv"
QUESTIONS_GENERATOR_CSV = DATA_DIR / "questions_generator.csv"
