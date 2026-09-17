# Asynchronous Activity 1: Student Early Warning Tool Using KNIME

This folder contains the KNIME submission for CS0065 Intelligent Systems, Asynchronous Activity 1. The project demonstrates three classification workflows for identifying students who may need early academic support from attendance and assessment results.

## Files

- `DemoEarlyWarningTool.knwf` — exported KNIME workflow package containing Logistic Regression, Decision Tree, and Random Forest learner/predictor branches with Scorer nodes.
- `student_performance_knime.csv` — included CSV dataset for the student early-warning use case.
- `Gorospe_Paolo_KNIME_GitHub_Evidence.pdf` — evidence PDF showing the project preparation, Git commands, and GitHub verification.
- `student_performance_model.py` — optional Python comparison script using the same four features and target column.

## Algorithms

The included workflow compares three classifiers:

- Logistic Regression
- Decision Tree
- Random Forest

Each branch uses the student performance features and evaluates predictions with a Scorer node.

## How to Run

1. Download `DemoEarlyWarningTool.knwf` from this folder.
2. In KNIME Analytics Platform, select **File > Import KNIME Workflow** and choose the downloaded `.knwf` file.
3. Open the workflow and configure the input. If the imported package shows its example Table Reader, replace it with or configure a CSV Reader and select `student_performance_knime.csv` from this folder.
4. Confirm that the CSV Reader nodes use `student_performance_knime.csv` from this folder.
5. Confirm `risk_status` is the target column and execute the nodes from left to right.
6. Open the Scorer node for each algorithm to review its confusion matrix and classification statistics.

The packaged workflow is a portable exported KNIME workflow. KNIME may require the standard KNIME Base Nodes extension and may ask for local file-path configuration after import.

## Dataset Columns

`student_id`, `attendance`, `quiz_score`, `assignment_score`, `exam_score`, and `risk_status`.

`risk_status` is the classification target (`At Risk` or `Not At Risk`). The included file has 30 student records: 14 `At Risk` and 16 `Not At Risk`.

## Author

Paolo Gorospe

## Course and Section

CS0065 — Intelligent Systems, AN43
