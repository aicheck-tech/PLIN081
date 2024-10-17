import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import classification_report
from collections import Counter


from sentence_transformers import SentenceTransformer


def majority_vote(labels):
    """Return the most common label from a list of labels."""
    return Counter(labels).most_common(1)[0][0]


def embed_texts(model, texts):
    """Convert texts to embeddings using the provided model."""
    return model.encode(texts)


def find_top_k_embeddings(test_embedding, train_embeddings, k=5):
    """Find indices of top k embeddings most similar to the test embedding."""
    similarities = cosine_similarity([test_embedding], train_embeddings)[0]
    return np.argsort(similarities)[-k:]


def predict_label(test_embedding, train_embeddings, train_labels, k=5):
    """Predict label for a single test embedding."""
    top_indices = find_top_k_embeddings(test_embedding, train_embeddings, k)
    top_labels = train_labels[top_indices]
    return majority_vote(top_labels)


def main():
    # Load dataset
    categories = ['sci.space', 'comp.graphics']
    data = fetch_20newsgroups(subset='all', categories=categories,
                              remove=('headers', 'footers', 'quotes'))

    # Split dataset
    X_train_texts, X_test_texts, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )

    # Initialize the semantic embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Embed training and test texts
    X_train_embeddings = embed_texts(model, X_train_texts)
    X_test_embeddings = embed_texts(model, X_test_texts)

    # Predict labels for test data
    y_pred = [
        predict_label(X_test_embeddings[i], X_train_embeddings, y_train)
        for i in range(len(X_test_embeddings))
    ]

    # Evaluate predictions
    print(classification_report(y_test, y_pred, target_names=data.target_names))


if __name__ == "__main__":
    main()
