# main.py

from app.models.data_preprocessing import (
    load_data,
    select_columns,
    handle_missing_rows,
    feature_engineering,
    get_features_and_labels
)

from app.models.model import train_model
from app.models.artifacts_saver import save_model, save_label_encoder


def run_pipeline():
    file_path = "data/data_collected.json"

    # Load + preprocess
    df = load_data(file_path)
    df = select_columns(df)
    df = handle_missing_rows(df)
    df = feature_engineering(df)

    # Features + labels
    X, y = get_features_and_labels(df)

    # Train
    model, encoder = train_model(X, y)

    # Save
    save_model(model, "data/model.pkl")
    save_label_encoder(encoder, "data/label_encoder.pkl")


if __name__ == "__main__":
    run_pipeline()