"""Transparent scholarship eligibility and ranking. All amounts are illustrative."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
REQUIRED = ["application_id", "grade_average", "annual_household_income",
            "activity_count", "document_status", "enrolled", "resident"]


def rank_applications(source: pd.DataFrame) -> pd.DataFrame:
    missing_columns = set(REQUIRED) - set(source.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")
    df = source[REQUIRED].copy()
    df["application_id"] = df["application_id"].astype("string").str.strip()
    if df["application_id"].isna().any() or df["application_id"].eq("").any():
        raise ValueError("Every application needs an application_id")
    if df["application_id"].duplicated().any():
        raise ValueError("application_id values must be unique")

    for column in ["grade_average", "annual_household_income", "activity_count"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    for column in ["document_status", "enrolled", "resident"]:
        df[column] = df[column].astype("string").str.strip().str.lower()

    grade_ok = df.grade_average.between(0, 100)
    income_ok = df.annual_household_income.between(0, 1000000)
    activity_ok = df.activity_count.between(0, 20) & df.activity_count.mod(1).eq(0)
    docs_ok = df.document_status.isin(["verified", "pending", "missing"])
    enrollment_ok = df.enrolled.isin(["yes", "no"])
    residence_ok = df.resident.isin(["yes", "no"])
    valid = grade_ok & income_ok & activity_ok & docs_ok & enrollment_ok & residence_ok
    eligible = (valid & df.grade_average.ge(75) &
                df.annual_household_income.le(60000) &
                df.document_status.eq("verified") &
                df.enrolled.eq("yes") & df.resident.eq("yes"))

    reasons = []
    for i in df.index:
        row_reasons = []
        for name, check in [("grade", grade_ok), ("income", income_ok),
                            ("activities", activity_ok), ("documents", docs_ok),
                            ("enrollment", enrollment_ok), ("residency", residence_ok)]:
            if not check.loc[i]:
                row_reasons.append(f"invalid or missing {name}")
        if valid.loc[i]:
            if df.at[i, "grade_average"] < 75:
                row_reasons.append("grade below 75")
            if df.at[i, "annual_household_income"] > 60000:
                row_reasons.append("income above 60000")
            if df.at[i, "document_status"] != "verified":
                row_reasons.append("documents not verified")
            if df.at[i, "enrolled"] != "yes":
                row_reasons.append("not enrolled")
            if df.at[i, "resident"] != "yes":
                row_reasons.append("not resident")
        reasons.append("eligible" if not row_reasons else "; ".join(row_reasons))

    df["validation_status"] = np.where(valid, "valid", "needs correction")
    df["eligibility_status"] = np.where(eligible, "eligible", "not eligible / review")
    df["reason"] = reasons

    # Fixed bounds ensure a record's score never changes when another record is added.
    grade_component = ((df.grade_average - 75) / 25).clip(0, 1)
    need_component = ((60000 - df.annual_household_income) / 60000).clip(0, 1)
    activity_component = (df.activity_count / 5).clip(0, 1)
    df["grade_points"] = np.where(eligible, 45 * grade_component, np.nan)
    df["need_points"] = np.where(eligible, 40 * need_component, np.nan)
    df["activity_points"] = np.where(eligible, 15 * activity_component, np.nan)
    df["weighted_score"] = (df.grade_points + df.need_points + df.activity_points).round(4)

    # Comparison method: simple categorical points, using the same eligibility gate.
    rule_grade = np.select([df.grade_average.ge(90), df.grade_average.ge(80)], [45, 30], default=15)
    rule_need = np.select([df.annual_household_income.le(20000),
                           df.annual_household_income.le(40000)], [40, 25], default=10)
    rule_activity = np.select([df.activity_count.ge(5), df.activity_count.ge(2)], [15, 10], default=0)
    df["rule_score"] = np.where(eligible, rule_grade + rule_need + rule_activity, np.nan)

    df["eligible_sort"] = np.where(eligible, 0, 1)
    df = df.sort_values(["eligible_sort", "weighted_score", "grade_average",
                         "annual_household_income", "application_id"],
                        ascending=[True, False, False, True, True],
                        na_position="last", kind="stable").reset_index(drop=True)
    df["weighted_rank"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    count = int(eligible.sum())
    df.loc[:count - 1, "weighted_rank"] = range(1, count + 1)
    comparison = df.loc[df.eligibility_status.eq("eligible")].sort_values(
        ["rule_score", "grade_average", "annual_household_income", "application_id"],
        ascending=[False, False, True, True], kind="stable")
    df["rule_rank"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    df.loc[comparison.index, "rule_rank"] = range(1, len(comparison) + 1)
    return df.drop(columns="eligible_sort")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank scholarship applications for human review")
    parser.add_argument("input", nargs="?", type=Path, default=ROOT / "applications.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "ranked_results.csv")
    args = parser.parse_args()
    ranked = rank_applications(pd.read_csv(args.input))
    ranked.to_csv(args.output, index=False)
    comparison = ranked.loc[ranked.eligibility_status.eq("eligible"),
                            ["application_id", "weighted_score", "weighted_rank", "rule_score", "rule_rank"]].copy()
    comparison["rank_change"] = comparison.rule_rank - comparison.weighted_rank
    comparison.to_csv(args.output.with_name("comparison.csv"), index=False)
    print(f"{len(ranked)} records; {len(comparison)} eligible; wrote {args.output}")


if __name__ == "__main__":
    main()
