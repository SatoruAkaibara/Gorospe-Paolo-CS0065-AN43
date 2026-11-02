"""TA4: KR, RBR and CBR - Paolo C. Gorospe, AN43.
Run: python TA4_Gorospe.py (manual revision)
Or:  python TA4_Gorospe.py --demo (reproducible example)
Uses only the Python standard library. Cases are retained in memory.
"""
from copy import deepcopy
import sys

# Task 1A: five facts, grouped into three categories.
facts = {
    "environment": {"temperature_c": 32, "humidity_pct": 85,
                    "is_raining": True},
    "room": {"is_occupied": True},
    "equipment": {"aircon_available": True},
}


# Task 2A: each function implements one IF-THEN rule.
def rule_hot(f):
    if (f["environment"]["temperature_c"] > 30
            and f["room"]["is_occupied"]
            and f["equipment"]["aircon_available"]):
        return "Turn on the aircon."


def rule_humid(f):
    if (f["environment"]["humidity_pct"] > 70
            and f["room"]["is_occupied"]
            and f["equipment"]["aircon_available"]):
        return "Use the aircon's dry mode."


def rule_rain(f):
    if f["environment"]["is_raining"]:
        return "Bring an umbrella."


def rule_empty(f):
    if not f["room"]["is_occupied"]:
        return "Keep cooling equipment off in the empty room."


# Task 2B: check ALL rules against a working-memory snapshot.
def infer(f):
    working_memory = deepcopy(f)
    actions, trace = [], []
    for rule in (rule_hot, rule_humid, rule_rain, rule_empty):
        action = rule(working_memory)
        trace.append((rule.__name__, bool(action)))
        if action and action not in actions:
            actions.append(action)
    return actions, trace


# CBR uses Boolean features so all five comparisons have equal weight.
def features(f):
    return {"hot": f["environment"]["temperature_c"] > 30,
            "humid": f["environment"]["humidity_pct"] > 70,
            "raining": f["environment"]["is_raining"],
            "occupied": f["room"]["is_occupied"],
            "aircon": f["equipment"]["aircon_available"]}


# Task 3A: three illustrative past cases, each with a solution.
case_base = [
    {"id": 1, "problem": {"hot": True, "humid": True,
     "raining": False, "occupied": True, "aircon": True},
     "solution": "Turn on the aircon and use dry mode."},
    {"id": 2, "problem": {"hot": False, "humid": True,
     "raining": True, "occupied": True, "aircon": False},
     "solution": "Use a fan and bring an umbrella."},
    {"id": 3, "problem": {"hot": False, "humid": False,
     "raining": False, "occupied": False, "aircon": True},
     "solution": "Keep cooling equipment off."},
]


# Retrieve: fraction of matching features; ties keep the first case.
def similarity(problem, past):
    if not problem:
        raise ValueError("At least one problem feature is required.")
    matches = sum(k in past and past[k] == v
                  for k, v in problem.items())
    return matches / len(problem)


def retrieve(problem, cases):
    if not cases:
        raise ValueError("The case base is empty.")
    scores = [similarity(problem, c["problem"]) for c in cases]
    best_index = max(range(len(cases)), key=lambda i: scores[i])
    return cases[best_index], scores


# Task 3C: reuse the retrieved solution without changing its case.
def reuse(case):
    return case["solution"]


# Task 3D: a blank response keeps the solution unchanged.
def revise(solution, replacement):
    return replacement.strip() or solution


# Task 3E: retain an independent copy for later retrieval in this run.
def retain(problem, solution, cases):
    new_id = max((c["id"] for c in cases), default=0) + 1
    cases.append({"id": new_id, "problem": deepcopy(problem),
                  "solution": solution})
    return cases[-1]


def main():
    print("TA4 - Paolo C. Gorospe | AN43 | November 2, 2026")
    print("INPUT - Knowledge base (3 categories, 5 facts)")
    for category, values in facts.items():
        print(f"{category}: {values}")
    actions, trace = infer(facts)
    print("\nRBR PROCESS - Check every rule")
    for name, fired in trace:
        print(f"{name}: {'FIRED' if fired else 'not fired'}")
    print("Rule-Based Reasoning Actions:")
    for action in actions:
        print(f"- {action}")
    if not actions:
        print("- No rule matched.")

    problem = features(facts)
    cases = deepcopy(case_base)
    print("\nCBR INPUT - Features from the same knowledge base")
    print(problem)
    best, scores = retrieve(problem, cases)
    print("RETRIEVE - Matching features / 5")
    for case, score in zip(cases, scores):
        print(f"Case {case['id']}: {score:.0%} similarity")
    proposed = reuse(best)
    print(f"REUSE - Case {best['id']}: {proposed}")
    if "--demo" in sys.argv:
        replacement = proposed + " Bring an umbrella."
        print("REVISE - Demo manual adjustment: add umbrella advice.")
    else:
        replacement = input("REVISE - New solution (Enter to keep): ")
    final = revise(proposed, replacement)
    print(f"Final solution: {final}")
    before = len(cases)
    new_case = retain(problem, final, cases)
    print(f"RETAIN - Cases: {before} -> {len(cases)}")
    print(f"New case ID: {new_case['id']}")
    again, _ = retrieve(problem, cases)
    score = similarity(problem, again["problem"])
    print(f"RETRIEVE AGAIN - Case {again['id']}: {score:.0%} similarity")
    print("Retention lasts for this run; restarting restores 3 cases.")


if __name__ == "__main__":
    main()
