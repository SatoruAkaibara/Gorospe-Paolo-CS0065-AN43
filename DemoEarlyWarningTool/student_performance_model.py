from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "student_performance_knime.csv"
PIPELINE_FILE = BASE_DIR / "student_performance_pipeline.joblib"

FEATURES = [
    "attendance",
    "quiz_score",
    "assignment_score",
    "exam_score",
]
TARGET = "risk_status"


def main():
    data = pd.read_csv(CSV_FILE)

    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y,
    )

    models = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=2000, random_state=42)),
        ]),
        "Decision Tree": DecisionTreeClassifier(
            random_state=42,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
        ),
    }

    print(f"Loaded {len(data)} student records from {CSV_FILE.name}")
    print(f"Features: {', '.join(FEATURES)}")
    print(f"Target: {TARGET}")

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        print(f"\n{name}")
        print("-" * len(name))
        print(f"Accuracy: {accuracy_score(y_test, predictions):.3f}")
        print(
            "Precision for At Risk: "
            f"{precision_score(y_test, predictions, pos_label='At Risk', zero_division=0):.3f}"
        )
        print(
            "Recall for At Risk: "
            f"{recall_score(y_test, predictions, pos_label='At Risk', zero_division=0):.3f}"
        )
        print(
            "F1-score for At Risk: "
            f"{f1_score(y_test, predictions, pos_label='At Risk', zero_division=0):.3f}"
        )
        print("Confusion matrix:")
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions, zero_division=0))

    selected_model = models["Decision Tree"]
    selected_model.fit(X, y)
    joblib.dump(selected_model, PIPELINE_FILE)

    sample_student = pd.DataFrame([{
        "attendance": 55,
        "quiz_score": 48,
        "assignment_score": 52,
        "exam_score": 50,
    }])

    print(f"Saved trained pipeline to {PIPELINE_FILE.name}")
    print(f"Sample prediction: {selected_model.predict(sample_student)[0]}")


if __name__ == "__main__":
    main()
