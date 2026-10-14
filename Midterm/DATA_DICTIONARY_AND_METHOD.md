# Data dictionary and method

## Part 1 — Dataset roles

| Field | Type and allowed values | Role | Missing handling |
|---|---|---|---|
| `application_id` | Unique, nonempty text | Reporting ID and final tie breaker; not scored | Reject the upload |
| `grade_average` | Number from 0 to 100 | Eligibility and academic score | Hold for correction |
| `annual_household_income` | Number from 0 to 1,000,000, illustrative units | Eligibility and need score | Hold for correction |
| `activity_count` | Integer from 0 to 20 | Activity score | Hold for correction |
| `document_status` | `verified`, `pending`, `missing` | Eligibility evidence | Hold for review or correction |
| `enrolled` | `yes`, `no` | Eligibility | Hold for review or correction |
| `resident` | `yes`, `no` | Eligibility | Hold for review or correction |

There is **no required target label**: this is a decision support ranking, not supervised learning. Generated outputs are `validation_status`, `eligibility_status`, `reason`, three score components, `weighted_score`, `weighted_rank`, `rule_score`, and `rule_rank`. Identifiers are retained in every result. No applicant names, addresses, or document contents are stored in this example. Grade, income, and activities are sensitive in practice, so restrict access and avoid publishing applicant level results.

## Part 2 — Eligibility and scoring

The eligibility gate requires all of the following: valid fields; grade average **at least 75**; annual household income **at most 60,000**; verified documents; enrolled `yes`; resident `yes`. Boundary values 75 and 60,000 pass. Pending documents, missing values, malformed categories, or out-of-range values receive no rank and appear in the review section with a reason. No missing value is silently imputed.

For eligible records, the **primary weighted score** is from 0 to 100:

```text
grade points    = 45 × (grade_average − 75) / 25
need points     = 40 × (60,000 − annual_household_income) / 60,000
activity points = 15 × min(activity_count, 5) / 5
weighted score  = sum of the three components
```

The components are clipped to their valid 0–1 ranges. Fixed scales avoid score drift when the pool changes. The 45/40/15 weights give academics the largest share while recognizing financial need and involvement. They are proposed policy choices, not empirical findings.

The **comparison rule score** uses the same eligibility gate and adds categorical points:

| Criterion | Band | Points |
|---|---|---:|
| Grade | ≥90 / ≥80 / 75–79.9 | 45 / 30 / 15 |
| Income | ≤20,000 / ≤40,000 / 40,001–60,000 | 40 / 25 / 10 |
| Activities | ≥5 / ≥2 / 0–1 | 15 / 10 / 0 |

Both methods sort by score descending, then grade descending, income ascending, and application ID ascending. The ID resolves a complete tie deterministically. Rank is sequential review order, not a declaration that adjacent applicants differ meaningfully. Human reviewers can override it only with a recorded reason and the original score retained.

## Part 3 — KNIME workflow

`CSV Reader → Column Filter → Missing Value → Rule Engine → Math Formula → Normalizer → Sorter → Top k Row Filter`

Missing Value removes rows with missing numeric inputs; Rule Engine labels the remaining rows eligible or review. Math Formula computes the 45/40/15 weighted score; Normalizer scales that score to 0–1; Sorter places eligible rows first and applies score and tie breakers. Top k Row Filter keeps the top 24 rows, which are exactly the 24 eligible records in this bundled sample. If the dataset changes, recalculate the eligible count and update k. Python also validates uploads and exports a full audit table, including held records and the comparison method.

## Part 6 — Evaluation and reflection

| Check | Result |
|---|---|
| Validity | 60 synthetic records, 7 columns, 24 eligible, 1 with a missing field |
| Boundary | Grade 75 and income 60,000 pass; 74.9 and 60,001 fail |
| Missing/uncertain | Missing grade is held for correction; pending document is held for review |
| Ranking consistency | A score uses fixed bounds, so adding another applicant does not alter it |
| Comparison | Top weighted applicant: G7-059; top categorical rule applicant: G7-008; Spearman rank correlation: 0.863 |
| Weight sensitivity | Changing grade/need/activity weights from 45/40/15 to 40/45/15 keeps the same top five but swaps G7-008 and G7-039 in positions 2 and 3 |
| Explainability | Each eligible record has separate grade, need, and activity points; held records have a reason |

**Highest priority:** Verified eligibility documents and complete records must be checked before score priority. Among eligible applications, the example gives grades 45 points and need 40; the committee should decide these weights publicly before reviewing applicants.

**When no option satisfies every requirement:** Return an empty eligible list, keep all applications in the review table, and ask the committee to review requirements or request corrections. Never quietly waive a threshold.

**Ties, conflicts, overrides:** Apply the published tie breakers. If records conflict, pause that application and verify the source. Record the reviewer, date, reason, original rank, and final disposition for any override, and provide an appeal route.

**Interpretation and limits:** The methods generally agree but can change the ordering because rule score bands hide differences within bands. A higher score indicates priority under these chosen assumptions, not applicant worth or guaranteed eligibility. Synthetic data cannot validate fairness or predict real outcomes. Income should be contextualized by household size and locale; activities may reflect unequal opportunity. Test and audit the policy with real stakeholders before deployment.
