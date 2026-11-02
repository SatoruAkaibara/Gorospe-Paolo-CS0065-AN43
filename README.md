# Gorospe-Paolo-CS0065-AN43
Technical Assessment submissions for CS0065 - AN43

## Submission folders

- [Technical Assessments](Technical%20Assessments/) — TA1 random walk simulation, TA2 rule-based agent reports, and TA3 case-based intelligent tutoring system.
- [DemoEarlyWarningTool](DemoEarlyWarningTool/) — Asynchronous Activity 1 KNIME workflow, dataset, README, and evidence PDF.
- [Midterm](Midterm/) — Group 7 Scholarship Application Review: KNIME workflow, Python ranking, Streamlit web interface, dataset, results, and documentation.

## TA3: Case-Based Intelligent Tutoring System

By Gorospe and Gamboa. The tutor recommends feedback, worked examples, and practice for common errors in linear equations: sign changes, distribution, and division.

- [Assessment report (PDF)](Technical%20Assessments/TA3_Gorospe_Gamboa.pdf)
- [Python program](Technical%20Assessments/cbr_tutor.py)

The program starts with five fictional successful cases. It compares the error type, quiz score, and number of attempts using weighted similarity (50%, 30%, and 20%), retrieves a successful case with the same error, and adapts the practice workload. New cases are retained in JSON after a follow-up score is entered or left pending. Only cases with a follow-up score of at least 70 are eligible for future reuse.

### Run the program

Requires Python 3.10 or newer; no additional packages are needed. From the repository root:

```sh
python "Technical Assessments/cbr_tutor.py"
```

Run the repeatable demonstration with fictional inputs:

```sh
python "Technical Assessments/cbr_tutor.py" --demo
```

Interactive mode saves learned cases to `Technical Assessments/cases.json`. Use `--cases my_cases.json` to choose another location. Demo mode uses a temporary case file and leaves the interactive case base unchanged.
