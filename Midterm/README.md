# Midterm — Group 7 Scholarship Application Review

This decision-support project checks scholarship eligibility and ranks qualified applications for **human review**. It uses synthetic data and illustrative policy weights; it does not decide scholarship awards.

## Required outputs

| Requirement | Where to find it |
|---|---|
| 30–100 record dataset | [applications.csv](applications.csv) — 60 synthetic records with an application ID and six policy inputs. |
| Data dictionary | [DATA_DICTIONARY_AND_METHOD.md](DATA_DICTIONARY_AND_METHOD.md) — field roles, valid values, missing-value handling, eligibility rules, weights, and tie breakers. |
| KNIME workflow | [KNIME_Scholarship_Review.knwf](KNIME_Scholarship_Review.knwf) — importable eight-node workflow with the CSV bundled in its data area. |
| Python implementation | [ranking.py](ranking.py) — pandas/NumPy eligibility checks, weighted and rule-based scoring, ranking, and CSV exports. |
| Streamlit interface | [app.py](app.py) — upload or edit applications, run the ranking, inspect held records, compare methods, and download results. |
| Comparison table | [comparison.csv](comparison.csv) — weighted and rule-based scores and ranks for the 24 eligible records. |
| Short interpretation and limitations | The [evaluation and reflection section](DATA_DICTIONARY_AND_METHOD.md#part-6--evaluation-and-reflection) and the summary below. |

The complete 60-record output, including applications held for correction or review, is in [ranked_results.csv](ranked_results.csv).

## Run the project

Download or clone the repository and run these commands from `Midterm/` with Python 3.10 or newer:

```bash
python -m pip install -r requirements.txt
python ranking.py
python -m streamlit run app.py
```

`ranking.py` prints a record count and writes `ranked_results.csv` and `comparison.csv`. Streamlit opens the web interface locally.

For KNIME, import `KNIME_Scholarship_Review.knwf`, execute the workflow, and inspect the final **Top k Row Filter** output. Its path is **CSV Reader → Column Filter → Missing Value → Rule Engine → Math Formula → Normalizer → Sorter → Top k Row Filter**. The CSV Reader uses the workflow's bundled data area rather than a `D:` path.

## Result and interpretation

Of 60 synthetic applications, 24 pass the eligibility rules and one has a missing field. The weighted method ranks **G7-059** first; the comparison rule method ranks **G7-008** first. Their eligible ranks have Spearman correlation **0.863**, showing broad agreement but meaningful differences in review order.

KNIME normalizes its score to 0–1 and shows the top 24 rows for this sample. Python retains the raw weighted score and exports all 60 records with reasons for those held. The eligible applicant order matches. If the dataset changes, update KNIME's fixed Top k value after counting eligible records.

The thresholds and weights are examples. Income does not account for household size or local costs, and activity count does not capture opportunity or quality. A real committee should approve and audit the policy, verify records, allow corrections and appeals, and document human overrides.
