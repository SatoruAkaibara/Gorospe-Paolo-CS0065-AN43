# Gorospe-Paolo-CS0065-AN43
Technical Assessment submissions for CS0065 - AN43

## Submission folders

- [Technical Assessments](Technical%20Assessments/) — TA1 random walk simulation, TA2 rule-based agent reports, TA3 case-based intelligent tutoring system, and TA4 knowledge representation with rule-based and case-based reasoning.
- [DemoEarlyWarningTool](DemoEarlyWarningTool/) — Asynchronous Activity 1 KNIME workflow, dataset, README, and evidence PDF.
- [Midterm](Midterm/) — Group 7 Scholarship Application Review: KNIME workflow, Python ranking, Streamlit web interface, dataset, results, and documentation.

## TA4: Knowledge Representation, Rule-Based Reasoning, and Case-Based Reasoning

By Paolo C. Gorospe. A classroom comfort and weather assistant uses the same knowledge base to compare rule-based reasoning (RBR) and case-based reasoning (CBR).

- [Assessment report with code, reflection, and terminal screenshots (PDF)](Technical%20Assessments/TA4_Gorospe.pdf)
- [Python program](Technical%20Assessments/TA4_Gorospe.py)

The knowledge base contains five facts in three categories: environment, room, and equipment. Four IF–THEN rules generate cooling and rain advice. CBR compares five Boolean features against three past cases, then retrieves, reuses, revises, and retains a solution. The demonstration selects Case 1 at 80% similarity, adds umbrella advice, and retains Case 4, which matches the current problem at 100%.

### Run TA4

Requires Python 3; no additional packages are needed. From the repository root:

```sh
python "Technical Assessments/TA4_Gorospe.py"
```

Enter a replacement solution when prompted, or press Enter to keep the proposed solution. To reproduce the report's screenshots with the automatic demonstration revision:

```sh
python "Technical Assessments/TA4_Gorospe.py" --demo
```

New cases are retained in memory only for the current run. Restarting restores the three initial cases.

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
