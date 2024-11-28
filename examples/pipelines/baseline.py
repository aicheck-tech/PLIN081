import pickle
import logging
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score


# Paths
DATA = Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
VECTORIZER_PATH = DATA / "vectorizer.pkl"
MODEL_PATH = DATA / "model.pkl"


def save_pickle(obj: object, path: Path) -> None:
    """Saves an object to a file using pickle."""
    try:
        path.write_bytes(pickle.dumps(obj))
        logging.info(f"Saved object to {path}")
    except Exception as e:
        logging.error(f"Error saving to {path}: {e}")


def load_pickle(path: Path) -> object:
    """Loads an object from a pickle file."""
    try:
        return pickle.loads(path.read_bytes())
    except Exception as e:
        logging.error(f"Error loading from {path}: {e}")
        raise


def load_train_data() -> tuple[list[str], list[int]]:
    texts = ["This is a positive review", "This is a negative review",
             "Positive vibes here", "Not good, very negative",
             "I love this", "I hate this", "meh", "pche", "dunno", "nope", "no", "no way", "nope nope nope",
             "in love", "pretty", "nice!", "cool", "awesome", "amazing", "fantastic", "wonderful", "great",
             ]
    labels = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    return texts, labels


def load_test_data() -> tuple[list[str], list[int]]:
    texts = ["This is a cool review", "This is a horrible review",
             "Feeling happy", "Bad bad bad, very bad",
             "I love your product", "I hate you"]
    labels = [1, 0, 1, 0, 1, 0]
    return texts, labels


def train_model(texts: list[str], labels: list[int],
                vectorizer_path: Path = VECTORIZER_PATH,
                model_path: Path = MODEL_PATH) -> None:
    vectorizer = CountVectorizer()
    instances = vectorizer.fit_transform(texts)

    classifier = MultinomialNB()
    classifier.fit(instances, labels)

    save_pickle(vectorizer, vectorizer_path)
    save_pickle(classifier, model_path)


def eval_model(texts: list[str], labels: list[int],
               vectorizer_path: Path = VECTORIZER_PATH, model_path: Path = MODEL_PATH
               ) -> None:
    vectorizer = load_pickle(vectorizer_path)
    classifier = load_pickle(model_path)

    instances = vectorizer.transform(texts)
    y_pred = classifier.predict(instances)

    logging.info("Accuracy: %s", accuracy_score(labels, y_pred))
    logging.info("\nClassification Report:\n%s", classification_report(labels, y_pred))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

    train_texts, train_labels = load_train_data()
    test_texts, test_labels = load_test_data()

    train_model(train_texts, train_labels)
    eval_model(test_texts, test_labels)