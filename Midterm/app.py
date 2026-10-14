"""Human-review interface for the Group 7 scholarship example."""
from pathlib import Path
import pandas as pd
import streamlit as st
from ranking import rank_applications, REQUIRED

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Scholarship Review | Group 7", layout="wide")
st.title("Scholarship application review")
st.caption("Illustrative decision support. Scores organize applications; people make award decisions.")

uploaded = st.file_uploader("Upload application CSV", type="csv")
if uploaded:
    try:
        records = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"Could not read CSV: {exc}")
        st.stop()
else:
    records = pd.read_csv(ROOT / "applications.csv")

st.write("Edit the table below, or upload a CSV with these columns: " + ", ".join(REQUIRED))
edited = st.data_editor(records, num_rows="dynamic", hide_index=True, width="stretch")

if st.button("Rank applications", type="primary"):
    try:
        ranked = rank_applications(edited)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    eligible = ranked[ranked.eligibility_status.eq("eligible")]
    review = ranked[~ranked.eligibility_status.eq("eligible")]
    st.metric("Eligible for ranking", len(eligible))
    st.subheader("Ranked list for human review")
    st.dataframe(eligible[["weighted_rank", "application_id", "weighted_score",
                           "grade_points", "need_points", "activity_points",
                           "grade_average", "annual_household_income", "activity_count"]],
                 hide_index=True, width="stretch")
    st.download_button("Download complete ranked results", ranked.to_csv(index=False),
                       file_name="ranked_results.csv", mime="text/csv")
    st.subheader("Comparison with rule-based scoring")
    st.dataframe(eligible[["application_id", "weighted_rank", "weighted_score",
                           "rule_rank", "rule_score"]], hide_index=True, width="stretch")
    st.subheader("Applications needing correction or eligibility review")
    st.dataframe(review[["application_id", "validation_status", "eligibility_status", "reason"]],
                 hide_index=True, width="stretch")
    st.info("Eligibility: grade ≥75; income ≤60,000; verified documents; enrolled and resident. "
            "Weighted score: 45% grade, 40% financial need, 15% activities. "
            "Ties use higher grade, lower income, then application ID. "
            "Pending documents and invalid fields are held for human review.")
