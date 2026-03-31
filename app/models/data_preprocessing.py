# src/data_preprocessing.py

import pandas as pd
import json


def load_data(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[['query', 'original_response', 'hallucination_score',
               'decision', 'retrieved_docs']]


def handle_missing_rows(df: pd.DataFrame) -> pd.DataFrame:
    def fill_missing_rows(row):
        if row['decision'] in ['NO_CONTENT', 'OUT_OF_SCOPE']:
            row['hallucination_score'] = 0.0
            row['original_response'] = ""
        return row

    return df.apply(fill_missing_rows, axis=1)


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df['response_length'] = df['original_response'].apply(len)
    df['num_docs'] = df['retrieved_docs'].apply(len)

    df['avg_doc_length'] = df['retrieved_docs'].apply(
        lambda docs: sum(len(d) for d in docs) / len(docs) if len(docs) > 0 else 0
    )

    return df


def get_features_and_labels(df: pd.DataFrame):
    features = [
        'hallucination_score',
        'response_length',
        'num_docs',
        'avg_doc_length'
    ]

    X = df[features]
    y = df['decision']

    return X, y