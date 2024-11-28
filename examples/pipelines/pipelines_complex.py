import logging
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler

from baseline import DATA
from pipelines_basic import experiment

PIPELINE_PATH = DATA / "text_classification_pipeline.joblib"


def create_pipeline() -> Pipeline:
    """Creates a text classification pipeline with multiple vectorizers."""
    # Define the feature extraction with two vectorizers
    feature_union = FeatureUnion([
        ('count_vectorizer', CountVectorizer()),  # Step 1a: Count vectorizer
        ('tfidf_vectorizer', TfidfVectorizer())   # Step 1b: TF-IDF vectorizer
    ])

    # Add a FunctionTransformer to convert sparse to dense before scaling
    dense_transformer = FunctionTransformer(lambda x: x.toarray(), accept_sparse=True)

    # Define the full pipeline
    pipeline = Pipeline([
        ('features', feature_union),                     # Merge vectorized outputs
        ('to_dense', dense_transformer),                 # Convert sparse to dense
        ('scaler', MinMaxScaler()),                    # Scale the features
        ('classifier', MultinomialNB())                 # Train the classifier
    ])
    return pipeline


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    experiment()
