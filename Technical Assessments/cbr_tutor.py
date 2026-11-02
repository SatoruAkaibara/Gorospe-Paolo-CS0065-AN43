"""
TA3 Intelligent Tutoring System using Case-Based Reasoning.
Python 3.10+, standard library only.
"""

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile

ERRORS = {
    "sign": "Incorrect sign when moving a term",
    "distribution": "Multiplier not applied to every term",
    "division": "Only one side divided by the coefficient",
}


def seed_cases():
    """Five fictional successful interventions."""
    examples = [
        (
            "sign",
            40,
            3,
            4,
            80,
            "Use the same inverse operation on both sides.",
            "x + 5 = 12 -> subtract 5 on both sides -> x = 7.",
        ),
        (
            "sign",
            55,
            2,
            3,
            85,
            "Write the inverse operation before simplifying.",
            "x - 4 = 9 -> add 4 on both sides -> x = 13.",
        ),
        (
            "distribution",
            50,
            3,
            4,
            80,
            "Multiply every term inside the parentheses.",
            "2(x + 3) = 14 -> 2x + 6 = 14 -> x = 4.",
        ),
        (
            "division",
            60,
            2,
            3,
            90,
            "Divide both sides by the coefficient of x.",
            "3x = 18 -> 3x / 3 = 18 / 3 -> x = 6.",
        ),
        (
            "sign",
            75,
            1,
            2,
            95,
            "Solve independently, then substitute to check.",
            "x + 8 = 15 -> x = 7; check: 7 + 8 = 15.",
        ),
    ]
    return [
        {
            "id": f"C{i:03d}",
            "problem": {"error": error, "score": score, "attempts": attempts},
            "solution": {
                "feedback": feedback,
                "example": example,
                "practice_count": count,
            },
            "outcome": {"post_score": post, "status": "successful"},
            "source": "fictional_seed",
        }
        for i, (error, score, attempts, count, post, feedback, example) in enumerate(
            examples, 1
        )
    ]


def validate_problem(problem):
    if not isinstance(problem, dict) or problem.get("error") not in ERRORS:
        raise ValueError("Choose sign, distribution, or division.")
    for field, low, high in (("score", 0, 100), ("attempts", 1, 5)):
        value = problem.get(field)
        if type(value) is not int or not low <= value <= high:
            raise ValueError(f"{field} must be an integer from {low} to {high}.")


def similarity(problem, past):
    """Weighted similarity in [0, 1]."""
    validate_problem(problem)
    validate_problem(past)
    error_match = float(problem["error"] == past["error"])
    score_match = 1 - abs(problem["score"] - past["score"]) / 100
    attempt_match = 1 - abs(problem["attempts"] - past["attempts"]) / 4
    return 0.50 * error_match + 0.30 * score_match + 0.20 * attempt_match


def retrieve(problem, cases):
    """Rank all cases; reuse only successful cases with the same error."""
    ranked = sorted(
        [(similarity(problem, c["problem"]), c) for c in cases],
        key=lambda item: (item[0], item[1]["id"]),
        reverse=True,
    )
    eligible = [
        (score, c)
        for score, c in ranked
        if c["problem"]["error"] == problem["error"]
        and c["outcome"]["status"] == "successful"
    ]
    if not eligible:
        raise ValueError("No successful case for this error. Ask a tutor.")
    return eligible[0][1], ranked


def adapt(problem, case):
    """Reuse feedback/example; adjust practice to current support needs."""
    validate_problem(problem)
    solution = deepcopy(case["solution"])
    count = 3
    if problem["score"] < 50:
        count += 2
    if problem["attempts"] >= 3:
        count += 2
    solution["practice_count"] = count
    return solution


def validate_cases(cases):
    if not isinstance(cases, list):
        raise ValueError("Case file must contain a JSON list.")
    seen = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Each case must be an object.")
        case_id = case.get("id", "")
        if (
            not isinstance(case_id, str)
            or len(case_id) < 4
            or case_id[0] != "C"
            or not case_id[1:].isascii()
            or not case_id[1:].isdigit()
            or case_id in seen
        ):
            raise ValueError("Case IDs must be unique, e.g. C001.")
        seen.add(case_id)
        validate_problem(case.get("problem"))
        solution = case.get("solution", {})
        if not isinstance(solution, dict):
            raise ValueError("Missing solution object.")
        if any(
            not isinstance(solution.get(k), str) or not solution[k].strip()
            for k in ("feedback", "example")
        ):
            raise ValueError("Each solution needs feedback and an example.")
        count = solution.get("practice_count")
        if type(count) is not int or not 1 <= count <= 20:
            raise ValueError("practice_count must be 1 to 20.")
        outcome = case.get("outcome", {})
        if not isinstance(outcome, dict):
            raise ValueError("Missing outcome object.")
        post = outcome.get("post_score")
        if post is not None and (type(post) is not int or not 0 <= post <= 100):
            raise ValueError("post_score must be 0 to 100, or null.")
        expected = (
            "pending"
            if post is None
            else "successful"
            if post >= 70
            else "needs_review"
        )
        if outcome.get("status") != expected:
            raise ValueError("Outcome status does not match post_score.")


def load_cases(path):
    if not path.exists():
        return seed_cases()
    cases = json.loads(path.read_text(encoding="utf-8"))
    validate_cases(cases)
    return cases


def save_cases(path, cases):
    """Replace atomically, so an interrupted write does not truncate JSON."""
    validate_cases(cases)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=path.name + ".",
            suffix=".tmp",
            delete=False,
        ) as file:
            temp_name = file.name
            json.dump(cases, file, indent=2)
            file.write("\n")
        os.replace(temp_name, path)
    finally:
        if temp_name and Path(temp_name).exists():
            Path(temp_name).unlink()


def retain(path, cases, problem, solution, post_score, source):
    number = max((int(c["id"][1:]) for c in cases), default=0) + 1
    status = (
        "pending"
        if post_score is None
        else "successful"
        if post_score >= 70
        else "needs_review"
    )
    new_case = {
        "id": f"C{number:03d}",
        "problem": deepcopy(problem),
        "solution": deepcopy(solution),
        "outcome": {"post_score": post_score, "status": status},
        "source": source,
    }
    updated = cases + [new_case]
    save_cases(path, updated)
    return new_case, updated


def display_plan(problem, case, ranked, solution):
    print("\n1. NEW PROBLEM | Linear equations")
    print(f"Error: {ERRORS[problem['error']]}")
    print(f"Quiz score: {problem['score']}/100 | Attempts: {problem['attempts']}")
    print("\n2. RETRIEVAL | Ranked similarity")
    for score, past in ranked:
        eligible = (
            past["problem"]["error"] == problem["error"]
            and past["outcome"]["status"] == "successful"
        )
        flag = "eligible" if eligible else "excluded"
        print(
            f"{past['id']}: {score * 100:5.1f}% | {past['problem']['error']:<12} | {flag}"
        )
    print(
        f"Retrieved: {case['id']} | Original practice: {case['solution']['practice_count']} questions"
    )
    print("\n3. ADAPTED FINAL SOLUTION")
    print(solution["feedback"])
    print("Example: " + solution["example"])
    print(
        f"Practice: {solution['practice_count']} questions (base 3; +2 if score <50; +2 if attempts >=3)."
    )
    print("Check every answer by substituting x into the original equation.")


def display_cases(cases):
    print(f"\n5. UPDATED CASE BASE | {len(cases)} cases")
    for case in cases:
        p, out = case["problem"], case["outcome"]
        post = "pending" if out["post_score"] is None else out["post_score"]
        print(
            f"{case['id']} | {p['error']:<12} | pre {p['score']:3} | attempts {p['attempts']} | post {str(post):>7} | {out['status']}"
        )


def read_int(prompt, low, high, optional=False):
    while True:
        value = input(prompt).strip()
        if optional and not value:
            return None
        try:
            number = int(value)
            if low <= number <= high:
                return number
        except ValueError:
            pass
        print(f"Enter a whole number from {low} to {high}.")


def run(path, demo=False):
    cases = load_cases(path)
    print("TA3 | CASE-BASED INTELLIGENT TUTORING SYSTEM")
    if demo:
        print("SIMULATED DEMO | Fictional data; temporary case file.")
        problem = {"error": "sign", "score": 35, "attempts": 4}
    else:
        print("Scope: linear equations; error type is identified by the user.")
        for number, (key, label) in enumerate(ERRORS.items(), 1):
            print(f" {number}. {label} ({key})")
        choice = read_int("Error type (1-3): ", 1, 3)
        problem = {
            "error": list(ERRORS)[choice - 1],
            "score": read_int("Quiz score (0-100): ", 0, 100),
            "attempts": read_int("Attempts (1-5): ", 1, 5),
        }

    case, ranked = retrieve(problem, cases)
    solution = adapt(problem, case)
    display_plan(problem, case, ranked, solution)

    print("\n4. REVIEW AND RETAIN")
    if demo:
        post = 80
        print("Simulated follow-up quiz: 80/100.")
    else:
        print("After practicing, enter a follow-up quiz score.")
        post = read_int(
            "Score (0-100; Enter if not yet tested): ", 0, 100, optional=True
        )

    new_case, updated = retain(
        path,
        cases,
        problem,
        solution,
        post,
        "simulated_demo" if demo else "user_reported",
    )
    print(f"New case saved: {new_case['id']} | {new_case['outcome']['status']}")
    if post is None or post < 70:
        print("Tutor review needed; this case is excluded from future reuse.")

    display_cases(updated)
    reloaded = load_cases(path)
    print(f"\nPersistence verified: {len(reloaded)} cases reloaded from JSON.")

    if demo:
        match, ranks = retrieve(problem, reloaded)
        print(
            f"Same problem after learning: {match['id']} at {ranks[0][0] * 100:.1f}% similarity."
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).with_name("cases.json"),
    )
    args = parser.parse_args()
    try:
        if args.demo:
            with tempfile.TemporaryDirectory() as folder:
                run(Path(folder) / "demo_cases.json", demo=True)
        else:
            run(args.cases.resolve())
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    except (EOFError, KeyboardInterrupt):
        parser.exit(1, "\nCancelled before completion.\n")


if __name__ == "__main__":
    main()