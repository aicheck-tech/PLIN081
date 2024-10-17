"""
ChatGPT instructions:

give me a scikit pipeline processing text, tokenizing, lemmatizing using scipy, make bag of words algorithm

also split data to train and test and evaluate

make minimal code comments, focus on modularity and code quality
check code is working
"""
import pickle
from pathlib import Path

import spacy
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


try:
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
except OSError:
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


class SpacyLemmatizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.nlp = nlp

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [' '.join([token.lemma_ for token in self.nlp(doc)]) for doc in X]


def train(X_train, y_train):
    pipeline = Pipeline([
        ('lemmatizer', SpacyLemmatizer()),
        ('vectorizer', CountVectorizer()),
        ('classifier', LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(X_train, y_train)
    return pipeline


def save(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)


def load(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    model_path = Path("model.pkl")
    data = fetch_20newsgroups(subset='all', categories=['sci.space', 'comp.graphics'],
                              remove=('headers', 'footers', 'quotes'))
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

    if model_path.is_file():
        model = load(model_path)
    else:
        model = train(X_train, y_train)
        save(model, model_path)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
