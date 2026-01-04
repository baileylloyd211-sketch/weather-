import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="Mirror Without Light", layout="centered")

st.title("Mirror Without Light — Diagnostic")
st.caption("Decodes feedback into: missing variable → distortion → smallest lever. No judgement, just signal.")

# ----------------------------
# Universal Question Bank (v1)
# ----------------------------
QUESTION_BANK = [
    # Baseline Stability
    {"id": "base_01", "text": "How many days this week did you wake up already feeling behind?", "variable": "Baseline", "weight": 1.2},
    {"id": "base_02", "text": "How often does one unexpected issue destabilize your whole day?", "variable": "Baseline", "weight": 1.3},
    {"id": "base_03", "text": "How often do you feel you are operating without a buffer?", "variable": "Baseline", "weight": 1.2},

    # Load / Capacity
    {"id": "load_01", "text": "How often do you feel drained before the main part of your day begins?", "variable": "Load", "weight": 1.4},
    {"id": "load_02", "text": "How often do you feel alert but unable to act?", "variable": "Load", "weight": 1.4},
    {"id": "load_03", "text": "How often do you delay rest because it feels unsafe or irresponsible?", "variable": "Load", "weight": 1.3},

    # Signal Clarity
    {"id": "sig_01", "text": "How often are you unsure whether what you’re doing is actually helping?", "variable": "Signal", "weight": 1.3},
    {"id": "sig_02", "text": "How often do you change behavior without knowing what caused the last outcome?", "variable": "Signal", "weight": 1.4},
    {"id": "sig_03", "text": "How often does silence feel like feedback?", "variable": "Signal", "weight": 1.3},

    # Feedback Safety
    {"id": "fb_01", "text": "How often do you avoid speaking up because it will create more work than relief?", "variable": "Feedback", "weight": 1.4},
    {"id": "fb_02", "text": "How often do issues get addressed only after they become unavoidable?", "variable": "Feedback", "weight": 1.4},
    {"id": "fb_03", "text": "How often do things smooth over without actually changing?", "variable": "Feedback", "weight": 1.3},

    # Incentives
    {"id": "inc_01", "text": "How often are you rewarded for endurance rather than improvement?", "variable": "Incentives", "weight": 1.3},
    {"id": "inc_02", "text": "How often do short-term fixes undermine longer-term outcomes?", "variable": "Incentives", "weight": 1.4},

    # Constraints
    {"id": "con_01", "text": "How often do plans fail because they ignore one obvious constraint?", "variable": "Constraints", "weight": 1.4},
    {"id": "con_02", "text": "How often do you feel judged for limits you didn’t choose?", "variable": "Constraints", "weight": 1.3},

    # Trajectory / Drift
    {"id": "dr_01", "text": "How often do weeks blur together without a sense of direction?", "variable": "Drift", "weight": 1.4},
    {"id": "dr_02", "text": "How often does effort result in continuation rather than relief?", "variable": "Drift", "weight": 1.5},
    {"id": "dr_03", "text": "How often do you feel like you’re maintaining position instead of changing it?", "variable": "Drift", "weight": 1.6},
]

SCALE = {
    0: "Never",
    1: "Rarely",
    2: "Sometimes",
    3: "Often",
    4: "Most days / Constant",
}

# ----------------------------
# Domain “lenses” (weights)
# ----------------------------
DOMAIN_WEIGHTS = {
    "Relationship": {"Baseline": 0.8, "Load": 1.5, "Signal": 1.1, "Feedback": 1.5, "Incentives": 1.2, "Constraints": 0.8, "Drift": 1.0},
    "Financial":     {"Baseline": 1.6, "Load": 1.3, "Signal": 1.2, "Feedback": 0.9, "Incentives": 1.1, "Constraints": 1.6, "Drift": 0.9},
    "Life Path":     {"Baseline": 0.9, "Load": 1.2, "Signal": 1.3, "Feedback": 1.0, "Incentives": 1.3, "Constraints": 0.9, "Drift": 1.7},
}

DOMAIN_TEXT = {
    "Financial": {
        "Constraints": {
            "missing": "Hard constraints are consuming planning capacity.",
            "distortion": "You read constraint effects as personal failure; survival moves look like ‘bad choices’ instead of predictable math.",
            "lever": "Stabilize one constraint first (deadline control, minimum buffer, or fixed essential cost).",
        },
        "Baseline": {
            "missing": "Baseline instability (no buffer/predictability) is driving volatility.",
            "distortion": "Every decision feels urgent; long-term planning collapses into short-horizon patching.",
            "lever": "Build predictability: one buffer, one routine bill day, one protected planning block.",
        },
        "Signal": {
            "missing": "You don’t have a clear scoreboard for what’s improving.",
            "distortion": "Effort gets spent without measurable gain; you keep changing tactics without learning.",
            "lever": "Define 2–3 financial signals (cash-on-hand days, fixed costs, debt minimums) and track weekly.",
        },
        "Load": {
            "missing": "Pre-load (stress + cognitive clutter) is eating the bandwidth required to plan.",
            "distortion": "You interpret shutdown as laziness; it’s capacity starvation.",
            "lever": "Reduce pre-load before planning: clear one recurring stressor, then plan in a short sprint (15 min).",
        },
        "Feedback": {
            "missing": "Feedback loops are too delayed or punishing to learn from.",
            "distortion": "You only learn after damage, so you start avoiding decisions.",
            "lever": "Shorten the loop: weekly review + one rule change at a time.",
        },
        "Incentives": {
            "missing": "Short-term relief is being rewarded more than stability.",
            "distortion": "You ‘win’ today in ways that guarantee next week’s loss.",
            "lever": "Change the reward: make stability the win (buffer-first, fixed-cost-first).",
        },
        "Drift": {
            "missing": "Effort is maintaining position, not changing state.",
            "distortion": "Busyness feels like progress; nothing accumulates.",
            "lever": "Pick one state-change target (buffer size, debt reduction, income step) and protect it.",
        },
    },

    "Relationship": {
        "Feedback": {
            "missing": "Feedback is not safe enough to correct early.",
            "distortion": "Small issues become identity fights; tone replaces topic.",
            "lever": "Create a safe loop: short check-ins, no verdicts, one issue at a time.",
        },
        "Load": {
            "missing": "Unspoken load is consuming relational capacity.",
            "distortion": "Capacity shortfall gets read as not caring or disrespect.",
            "lever": "Name load before meaning. ‘What’s draining you this week?’ comes first.",
        },
        "Signal": {
            "missing": "Signals are ambiguous or indirect.",
            "distortion": "You guess intent and act on guesses.",
            "lever": "Make signals explicit: ask for clarity, reflect back, confirm meaning.",
        },
        "Incentives": {
            "missing": "Peace/avoidance is being rewarded over honesty.",
            "distortion": "The relationship trains silence; resentment grows quietly.",
            "lever": "Reward truth gently: acknowledge honesty without punishment.",
        },
        "Baseline": {
            "missing": "Baseline instability is amplifying conflict intensity.",
            "distortion": "Every disagreement feels existential.",
            "lever": "Stabilize the baseline: sleep, routine, and time windows for hard talks.",
        },
        "Constraints": {
            "missing": "Real limits aren’t being spoken as limits.",
            "distortion": "Limits get interpreted as rejection.",
            "lever": "State constraints plainly: ‘I can’t do X right now’ without defense.",
        },
        "Drift": {
            "missing": "Connection is degrading through neglect rather than crisis.",
            "distortion": "You think it’s fine because nothing exploded.",
            "lever": "Add one recurring connection ritual that’s small and reliable.",
        },
    },

    "Life Path": {
        "Drift": {
            "missing": "Trajectory is unmanaged; effort is maintenance, not movement.",
            "distortion": "Endurance is mistaken for progress.",
            "lever": "Choose one measurable state-change and cut everything that doesn’t serve it for 30 days.",
        },
        "Signal": {
            "missing": "Your scoreboard for ‘better’ is unclear.",
            "distortion": "You keep optimizing behavior without learning what works.",
            "lever": "Define 3 signals: energy, stability, forward motion—track weekly.",
        },
        "Incentives": {
            "missing": "You’re being rewarded for compliance over alignment.",
            "distortion": "Life becomes performance; meaning erodes.",
            "lever": "Change the incentive map: stop feeding the loop that rewards you for shrinking.",
        },
        "Load": {
            "missing": "Load is too high for reflection and choice.",
            "distortion": "You interpret numbness as ‘this is just life.’",
            "lever": "Lower load enough to think: one subtraction before any addition.",
        },
        "Feedback": {
            "missing": "Feedback is noisy or unsafe, so you can’t calibrate.",
            "distortion": "You overcorrect based on fear instead of signal.",
            "lever": "Create a clean loop: weekly review + one experiment.",
        },
        "Baseline": {
            "missing": "Baseline instability keeps you reactive.",
            "distortion": "Everything feels urgent; nothing compounds.",
            "lever": "Stabilize the baseline: routine, buffer, recovery.",
        },
        "Constraints": {
            "missing": "Constraints are real but unowned, so you fight reality.",
            "distortion": "You blame yourself for physics.",
            "lever": "Name constraints and design inside them—then renegotiate one.",
        },
    },
}

# ----------------------------
# UI
# ----------------------------
domain = st.selectbox("Choose a lens", ["Relationship", "Financial", "Life Path"])

st.divider()
st.subheader("Universal Intake")
st.write("Answer in frequency. We’re measuring patterns, not morality.")

answers = {}
for q in QUESTION_BANK:
    val = st.slider(q["text"], 0, 4, 2, key=q["id"])
    st.caption(SCALE[val])
    answers[q["id"]] = val

def evaluate(domain_name: str, answers_dict: dict) -> dict:
    # Bucket weighted averages
    buckets = defaultdict(list)
    for q in QUESTION_BANK:
        buckets[q["variable"]].append(answers_dict[q["id"]] * q["weight"])
    avg = {k: sum(v) / len(v) for k, v in buckets.items()}

    # Apply lens weights
    w = DOMAIN_WEIGHTS[domain_name]
    weighted = {k: avg.get(k, 0.0) * w.get(k, 1.0) for k in avg}

    overall = sum(weighted.values()) / max(len(weighted), 1)
    if overall >= 3.0:
        risk = "High"
    elif overall >= 2.0:
        risk = "Moderate"
    else:
        risk = "Low"

   top_driver = drivers[0][0]  # e.g., "Constraints"
text = DOMAIN_TEXT[domain_name].get(top_driver, DOMAIN_TEXT[domain_name]["Drift"])
 

    return {
        "risk": risk,
        "missing": text["missing"],
        "distortion": text["distortion"],
        "lever": text["lever"],
        "drivers": drivers,
        "score": overall,
    }

st.divider()
if st.button("Decode Signals"):
    result = evaluate(domain, answers)

    st.header("Result")
    st.metric("Risk Level", result["risk"])

    st.subheader("Missing Variable")
    st.write(result["missing"])

    st.subheader("How the Signal is Distorted")
    st.write(result["distortion"])

    st.subheader("Smallest Lever That Changes Trajectory")
    st.write(result["lever"])

    st.subheader("Primary Drivers")
    for name, value in result["drivers"]:
        st.write(f"- **{name}**: {value:.2f}")

    st.caption(f"Composite score: {result['score']:.2f} (0–4 scale)")
