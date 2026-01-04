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
    "Relationship": {
        "missing": "Unmodeled load on each person’s regulatory capacity.",
        "distortion": "Capacity shortfall gets misread as intent (not caring / disrespect), triggering defensiveness and feedback suppression.",
        "lever": "No interpretation until load is named. Surface what’s draining capacity before assigning meaning.",
    },
    "Financial": {
        "missing": "Baseline instability + constraints consuming planning bandwidth.",
        "distortion": "Short-horizon survival behavior gets misread as irresponsibility; compounding penalties look like character failure instead of constraint math.",
        "lever": "Stabilize one constraint first (buffer, predictability, deadline control) before optimizing anything else.",
    },
    "Life Path": {
        "missing": "Signal ambiguity plus incentive pressure causing motion without state change.",
        "distortion": "Effort is mistaken for progress; endurance replaces direction; drift becomes ‘normal life.’",
        "lever": "Run an incentive + constraint audit. Change one driver of drift before adding more effort.",
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

    drivers = sorted(weighted.items(), key=lambda x: x[1], reverse=True)[:3]
    text = DOMAIN_TEXT[domain_name]

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
