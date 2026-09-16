# Asynchronous Activity 1: Student Early Warning Tool Using KNIME

This folder contains the KNIME submission for CS0065 Intelligent Systems, Asynchronous Activity 1. The project demonstrates a classification workflow for identifying students who may need early academic support.

## Files

- `DemoEarlyWarningTool.knwf` — exported KNIME workflow package. It contains a Decision Tree Learner, Decision Tree Predictor, Partitioning, and Scorer nodes.
- `student_performance_knime.csv` — included CSV dataset for the student early-warning use case.
- `Gorospe_Paolo_KNIME_GitHub_Evidence.pdf` — evidence PDF showing the project preparation, Git commands, and GitHub verification.

## Algorithm

The included workflow uses a Decision Tree classifier with a train/test partition and a Scorer node for evaluation. Decision Trees are appropriate here because the resulting rules can be inspected and explained to academic advisers.

## How to Run

1. Download `DemoEarlyWarningTool.knwf` from this folder.
2. In KNIME Analytics Platform, select **File > Import KNIME Workflow** and choose the downloaded `.knwf` file.
3. Open the workflow and configure the input reader. If the imported workflow shows a file path, point the CSV Reader to `student_performance_knime.csv` in this folder.
4. Confirm the target/risk column and execute the nodes from left to right.
5. Open the Scorer node to review the confusion matrix and classification statistics.

The packaged workflow is a portable exported KNIME workflow. KNIME may require the standard KNIME Base Nodes extension and may ask for local file-path configuration after import.

## Dataset Columns

`student_id`, `attendance_rate`, `average_grade`, `late_submissions`, `study_hours_per_week`, and `risk_status`.

`risk_status` is the classification target (`At Risk` or `Low Risk`).

## Author

Paolo Gorospe

## Course and Section

CS0065 — Intelligent Systems, AN43
