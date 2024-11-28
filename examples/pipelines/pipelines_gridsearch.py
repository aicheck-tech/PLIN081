import logging

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler

from baseline import DATA, load_train_data, load_test_data
from pipelines_basic import experiment, eval_model

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

    logging.info("Loading training and test data...")
    train_texts, train_labels = load_train_data()
    test_texts, test_labels = load_test_data()

    logging.info("Creating the pipeline...")
    pipeline = create_pipeline()

    # Define the parameter grid
    base_param_grid = {
        'features__count_vectorizer__max_features': [500, 1000],
        'features__tfidf_vectorizer__max_features': [500, 1000],
        'features__count_vectorizer__ngram_range': [(1, 1), (1, 2)],
        'features__tfidf_vectorizer__ngram_range': [(1, 1), (1, 2)],
        'scaler': [MinMaxScaler(), None]  # Try with and without scaling
    }

    # Classifier-specific grids
    classifiers = [
        (MultinomialNB(), {'classifier__alpha': [0.1, 1.0]}),
        (LogisticRegression(max_iter=500), {'classifier__C': [0.1, 1, 10]})
    ]

    param_grid = []
    for classifier, classifier_params in classifiers:
        grid = {**base_param_grid, 'classifier': [classifier], **classifier_params}
        param_grid.append(grid)

    # Grid search
    grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1_macro', verbose=3)
    logging.info("Performing grid search...")
    grid_search.fit(train_texts, train_labels)

    # Best parameters and evaluation
    logging.info(f"Best parameters: {grid_search.best_params_}")
    best_pipeline = grid_search.best_estimator_

    logging.info("Evaluating the best pipeline...")
    eval_model(best_pipeline, test_texts, test_labels)
