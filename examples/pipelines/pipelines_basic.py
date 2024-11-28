import logging
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump, load

from baseline import load_train_data, load_test_data, DATA

PIPELINE_PATH = DATA / "text_classification_pipeline.joblib"


def create_pipeline() -> Pipeline:
    """Creates a text classification pipeline."""
    return Pipeline([
        ('vectorizer', CountVectorizer()),  # Step 1: Vectorize text
        ('classifier', MultinomialNB())    # Step 2: Train the classifier
    ])


def train_model(pipeline: Pipeline, texts: list[str], labels: list[int], save_path: Path = PIPELINE_PATH) -> None:
    """Trains the pipeline and saves it."""
    pipeline.fit(texts, labels)
    dump(pipeline, save_path)
    logging.info(f"Pipeline saved to {save_path}")


def eval_model(pipeline: Pipeline, texts: list[str], labels: list[int]) -> None:
    """Evaluates the pipeline on test data."""
    y_pred = pipeline.predict(texts)
    logging.info("Accuracy: %s", accuracy_score(labels, y_pred))
    logging.info("\nClassification Report:\n%s", classification_report(labels, y_pred))


def experiment():
    logging.info("Loading training and test data...")
    train_texts, train_labels = load_train_data()
    test_texts, test_labels = load_test_data()

    logging.info("Traíning the model...")
    pipeline = create_pipeline()
    train_model(pipeline, train_texts, train_labels)

    logging.info("Evaluating the model...")
    loaded_pipeline = load(PIPELINE_PATH)
    eval_model(loaded_pipeline, test_texts, test_labels)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    experiment()
