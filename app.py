import random
from statistics import pstdev
import streamlit as st

# ==========================
# Streamlit App: One-File
# ==========================
st.set_page_config(page_title="3-Lens Diagnostic (25Q)", layout="centered")

st.title("3-Lens Diagnostic (25 questions)")
st.caption("Same scoring. Different lens. Randomized questions. Targeted readout + next-lever guidance.")

# --------------------------
# Universal Scale (0–4)
# --------------------------
SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

# --------------------------
# Universal Variables (shared)
# --------------------------
VARIABLE_WEIGHTS = {
    "Baseline": 1.2,
    "Clarity": 1.1,
    "Resources": 1.1,
    "Boundaries": 1.1,
    "Execution": 1.2,
    "Feedback": 1.0,
}

ZONES = {
    "RED": (0, 44.999),
    "YELLOW": (45, 69.999),
    "GREEN": (70, 100),
}

def zone_name(score_0_100: float) -> str:
    if score_0_100 < 45:
        return "RED"
    if score_0_100 < 70:
        return "YELLOW"
    return "GREEN"

def clamp(n, lo, hi):
    return max(lo, min(hi, n))

# --------------------------
# Question Bank (25 per lens)
# Each question: id, text, variable, weight, reverse
# reverse=True means higher answer is worse, so we flip: score = 4 - answer
# --------------------------
QUESTION_BANK = {
    "Interpersonal": [
        {"id":"i01","text":"How often do you feel tense before interacting with a specific person?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"i02","text":"How often does one conversation ruin your whole day?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"i03","text":"How often do you avoid a conversation you know you need to have?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"i04","text":"How clear are you about what you want from this relationship/situation?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"i05","text":"How often do you leave a talk unsure what was actually decided?","variable":"Clarity","weight":1.1,"reverse":True},
        {"id":"i06","text":"How often do you say “yes” when you mean “no”?","variable":"Boundaries","weight":1.4,"reverse":True},
        {"id":"i07","text":"How often do you tolerate behavior that you resent later?","variable":"Boundaries","weight":1.3,"reverse":True},
        {"id":"i08","text":"How often do you communicate your limits early rather than late?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"i09","text":"How supported do you feel by at least one person in your life?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"i10","text":"How often do you feel alone carrying the emotional load?","variable":"Resources","weight":1.2,"reverse":True},
        {"id":"i11","text":"How often do conflicts repeat without resolution?","variable":"Feedback","weight":1.2,"reverse":True},
        {"id":"i12","text":"How often do you reflect after conflict and adjust your approach?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"i13","text":"How often do you interpret neutral behavior as hostile?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"i14","text":"How often do you apologize to restore peace even when you weren’t wrong?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"i15","text":"How often do you directly ask for what you need?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"i16","text":"How often do you replay conversations in your head afterward?","variable":"Baseline","weight":1.0,"reverse":True},
        {"id":"i17","text":"How often do you feel respected in the dynamic?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"i18","text":"How often do you keep your word when you set a boundary?","variable":"Execution","weight":1.3,"reverse":False},
        {"id":"i19","text":"How often do you use sarcasm/withdrawal instead of stating the issue?","variable":"Execution","weight":1.1,"reverse":True},
        {"id":"i20","text":"How often do you feel you must perform to be valued?","variable":"Clarity","weight":1.0,"reverse":True},
        {"id":"i21","text":"How often do you choose timing/location to improve the odds of a good talk?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"i22","text":"How often do you communicate expectations before frustration builds?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"i23","text":"How often do you recover quickly after conflict?","variable":"Baseline","weight":1.1,"reverse":False},
        {"id":"i24","text":"How often do you ask clarifying questions instead of assuming intent?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"i25","text":"How often do you feel you’re walking on eggshells?","variable":"Baseline","weight":1.3,"reverse":True},
    ],
    "Financial": [
        {"id":"f01","text":"How often do you know your exact cash position (today) without guessing?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"f02","text":"How often do bills/fees surprise you?","variable":"Clarity","weight":1.2,"reverse":True},
        {"id":"f03","text":"How often do you feel like you’re one emergency away from collapse?","variable":"Baseline","weight":1.3,"reverse":True},
        {"id":"f04","text":"How often do you have a buffer (even small) after essentials?","variable":"Resources","weight":1.3,"reverse":False},
        {"id":"f05","text":"How often do you spend to regulate mood/stress?","variable":"Feedback","weight":1.1,"reverse":True},
        {"id":"f06","text":"How consistently do you track spending (even roughly)?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"f07","text":"How often do you miss due dates?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"f08","text":"How often do you avoid opening financial mail/notifications?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"f09","text":"How often do you negotiate rates, call providers, or challenge charges?","variable":"Execution","weight":1.0,"reverse":False},
        {"id":"f10","text":"How clear are you on your top 3 financial priorities this month?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f11","text":"How often do impulse purchases break your plan?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"f12","text":"How often do you review recurring subscriptions/auto-pay items?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"f13","text":"How often do you make a simple plan before spending (need vs want)?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f14","text":"How often does financial stress disrupt sleep/focus?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"f15","text":"How often do you feel your income is stable/predictable?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"f16","text":"How often do you know your minimum survival number per month?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"f17","text":"How often do you take one concrete financial action per week?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f18","text":"How often do you use a system (notes/app/spreadsheet) to reduce chaos?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"f19","text":"How often do you borrow/advance money to get through the month?","variable":"Resources","weight":1.1,"reverse":True},
        {"id":"f20","text":"How often do you postpone decisions until they become emergencies?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"f21","text":"How often do you set boundaries with others about money (loans, favors, guilt)?","variable":"Boundaries","weight":1.0,"reverse":False},
        {"id":"f22","text":"How often do you feel ashamed about money (and hide it)?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"f23","text":"How often do you have a realistic plan for the next 30 days?","variable":"Clarity","weight":1.2,"reverse":False},
        {"id":"f24","text":"How often do you follow that plan when stress hits?","variable":"Boundaries","weight":1.1,"reverse":False},
        {"id":"f25","text":"How often do you recover quickly after a financial hit?","variable":"Baseline","weight":1.1,"reverse":False},
    ],
    "Big Picture": [
        {"id":"b01","text":"How clear is your north star (what you’re building / aiming at)?","variable":"Clarity","weight":1.3,"reverse":False},
        {"id":"b02","text":"How often do you feel scattered across too many threads?","variable":"Baseline","weight":1.2,"reverse":True},
        {"id":"b03","text":"How often do you know the next smallest step without overthinking?","variable":"Clarity","weight":1.1,"reverse":False},
        {"id":"b04","text":"How often do you have enough energy/bandwidth to execute?","variable":"Resources","weight":1.2,"reverse":False},
        {"id":"b05","text":"How often do you burn time on tasks that don’t move the mission?","variable":"Boundaries","weight":1.2,"reverse":True},
        {"id":"b06","text":"How often do you ship something (even small) rather than refine forever?","variable":"Execution","weight":1.3,"reverse":False},
        {"id":"b07","text":"How often do you change direction mid-week?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"b08","text":"How often do you measure progress with a real metric (not vibes)?","variable":"Feedback","weight":1.2,"reverse":False},
        {"id":"b09","text":"How often do you review what worked and adjust your plan?","variable":"Feedback","weight":1.1,"reverse":False},
        {"id":"b10","text":"How often do you ignore obvious signals because they’re inconvenient?","variable":"Feedback","weight":1.0,"reverse":True},
        {"id":"b11","text":"How often do you protect focus time from interruptions?","variable":"Boundaries","weight":1.2,"reverse":False},
        {"id":"b12","text":"How often do you feel you’re operating without a buffer?","variable":"Resources","weight":1.1,"reverse":True},
        {"id":"b13","text":"How often do you have a simple weekly plan you can actually follow?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b14","text":"How often do you let urgency from others rewrite your priorities?","variable":"Boundaries","weight":1.1,"reverse":True},
        {"id":"b15","text":"How often do you know what to say “no” to right now?","variable":"Clarity","weight":1.0,"reverse":False},
        {"id":"b16","text":"How often do you feel meaningful momentum?","variable":"Baseline","weight":1.0,"reverse":False},
        {"id":"b17","text":"How often do you procrastinate on the one scary keystone task?","variable":"Execution","weight":1.2,"reverse":True},
        {"id":"b18","text":"How often do you have access to help/support/tools when stuck?","variable":"Resources","weight":1.0,"reverse":False},
        {"id":"b19","text":"How often do you document decisions so you don’t relitigate them?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"b20","text":"How often do you feel your environment is aligned with your goals?","variable":"Resources","weight":1.1,"reverse":False},
        {"id":"b21","text":"How often do you stop to simplify when complexity rises?","variable":"Feedback","weight":1.0,"reverse":False},
        {"id":"b22","text":"How often do you complete what you start?","variable":"Execution","weight":1.2,"reverse":False},
        {"id":"b23","text":"How often do you experience “mission drift” after setbacks?","variable":"Baseline","weight":1.1,"reverse":True},
        {"id":"b24","text":"How often do you pick one lever and push it hard for 7 days?","variable":"Execution","weight":1.1,"reverse":False},
        {"id":"b25","text":"How often do you feel the goal is real and reachable?","variable":"Clarity","weight":1.1,"reverse":False},
    ],
}

# --------------------------
# Scoring
# --------------------------
def compute_scores(questions, answers):
    """
    answers: dict[qid] -> int (0..4)
    returns: overall, per_variable dict with details
    """
    # collect per variable item scores in 0..4
    per_var_items = {}
    per_var_weights = {}
    per_var_raw_scores = {}  # for volatility

    # also keep a per-question scored list for "dominant distortions"
    scored_qs = []  # (variable, scored_0_4, weight, qdict, answer)

    for q in questions:
        qid = q["id"]
        if qid not in answers:
            continue
        a = int(answers[qid])
        s = (4 - a) if q.get("reverse", False) else a  # 0..4 higher is better
        v = q["variable"]
        w = float(q.get("weight", 1.0))

        per_var_items.setdefault(v, 0.0)
        per_var_weights.setdefault(v, 0.0)
        per_var_raw_scores.setdefault(v, [])

        per_var_items[v] += s * w
        per_var_weights[v] += w
        per_var_raw_scores[v].append(s)

        scored_qs.append((v, s, w, q, a))

    per_variable = {}
    for v, num in per_var_items.items():
        den = per_var_weights[v] if per_var_weights[v] else 1.0
        mean_0_4 = num / den
        pct = (mean_0_4 / 4.0) * 100.0

        # volatility: stdev of the 0..4 scores, scaled to 0..100
        raw_list = per_var_raw_scores.get(v, [])
        vol = 0.0
        if len(raw_list) >= 2:
            vol = (pstdev(raw_list) / 2.0) * 100.0
        vol = clamp(vol, 0, 100)

        per_variable[v] = {
            "mean_0_4": mean_0_4,
            "pct": pct,
            "zone": zone_name(pct),
            "volatility": vol,
        }

    # overall weighted by VARIABLE_WEIGHTS (only variables present)
    overall_num = 0.0
    overall_den = 0.0
    for v, info in per_variable.items():
        vw = float(VARIABLE_WEIGHTS.get(v, 1.0))
        overall_num += info["pct"] * vw
        overall_den += vw
    overall = (overall_num / overall_den) if overall_den else 0.0

    # Dominant distortions: lowest scored questions (after reverse handling)
    # We care about low "s" and high weight
    scored_qs_sorted = sorted(scored_qs, key=lambda t: (t[1], -t[2]))  # low score first, heavier weight first

    return overall, per_variable, scored_qs_sorted

def lens_readout_intro(lens: str) -> str:
    if lens == "Interpersonal":
        return "This readout interprets scores through **relationship dynamics**: tension, clarity, boundaries, follow-through."
    if lens == "Financial":
        return "This readout interprets scores through **stability + money control**: clarity, buffer, boundaries, execution."
    return "This readout interprets scores through **mission control**: clarity, focus, resources, execution, feedback loops."

def lens_translation(lens: str, variable: str) -> str:
    # Same variable names, but translated to lens language
    mapping = {
        "Interpersonal": {
            "Baseline": "Emotional baseline under contact",
            "Clarity": "What you want / what’s true",
            "Resources": "Support + emotional bandwidth",
            "Boundaries": "Limits + self-respect in action",
            "Execution": "Having the talk / doing the thing",
            "Feedback": "Repair, learning, reality-checking",
        },
        "Financial": {
            "Baseline": "Stability under money stress",
            "Clarity": "Numbers + priorities clarity",
            "Resources": "Income/buffer/tooling",
            "Boundaries": "Spending boundaries + exposure control",
            "Execution": "Bills/actions actually done",
            "Feedback": "Review, adjust, remove leaks",
        },
        "Big Picture": {
            "Baseline": "Stability + momentum",
            "Clarity": "North star + next step",
            "Resources": "Energy/support/environment",
            "Boundaries": "Focus protection + saying no",
            "Execution": "Shipping + completion",
            "Feedback": "Measurement + iteration",
        },
    }
    return mapping.get(lens, {}).get(variable, variable)

# --------------------------
# Session State
# --------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "setup"  # setup -> questions -> results
if "lens" not in st.session_state:
    st.session_state.lens = "Interpersonal"
if "q_order" not in st.session_state:
    st.session_state.q_order = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "active_questions" not in st.session_state:
    st.session_state.active_questions = []

def reset_run():
    st.session_state.q_order = []
    st.session_state.answers = {}
    st.session_state.idx = 0
    st.session_state.active_questions = []
    st.session_state.stage = "setup"

# --------------------------
# UI: Setup
# --------------------------
with st.sidebar:
    st.header("Controls")
    st.session_state.lens = st.selectbox("Choose a lens", list(QUESTION_BANK.keys()), index=list(QUESTION_BANK.keys()).index(st.session_state.lens))
    st.write("Questions per run: **25**")
    if st.button("Reset"):
        reset_run()

if st.session_state.stage == "setup":
    st.subheader("Pick the lens, then start.")
    st.write("- Interpersonal = relationships / conflict / boundaries")
    st.write("- Financial = stability / cashflow / decisions")
    st.write("- Big picture = mission / focus / execution")
    if st.button("Start 25 questions"):
        lens = st.session_state.lens
        bank = QUESTION_BANK[lens][:]
        random.shuffle(bank)
        # Exactly 25 asked (we have 25 in each lens right now)
        active = bank[:25]
        st.session_state.active_questions = active
        st.session_state.q_order = [q["id"] for q in active]
        st.session_state.idx = 0
        st.session_state.answers = {}
        st.session_state.stage = "questions"
        st.rerun()

# --------------------------
# UI: Questions
# --------------------------
if st.session_state.stage == "questions":
    lens = st.session_state.lens
    qs = st.session_state.active_questions
    total = len(qs)
    idx = st.session_state.idx

    st.subheader(f"{lens} lens — Question {idx+1} of {total}")
    st.progress((idx) / total)

    q = qs[idx]
    st.write(f"**{q['text']}**")
    st.caption(f"Measures: {lens_translation(lens, q['variable'])}")

    # default selection if answered
    current = st.session_state.answers.get(q["id"], None)
    options = list(SCALE_LABELS.keys())
    fmt = lambda x: SCALE_LABELS[x]

    choice = st.radio(
        "Choose one:",
        options,
        index=options.index(current) if current in options else 2,
        format_func=fmt,
        key=f"radio_{q['id']}"
    )

    st.session_state.answers[q["id"]] = int(choice)

    col1, col2, col3 = st.columns([1,1,2])
    with col1:
        if st.button("Back", disabled=(idx == 0)):
            st.session_state.idx = max(0, idx - 1)
            st.rerun()
    with col2:
        if st.button("Next", disabled=(idx >= total - 1)):
            st.session_state.idx = min(total - 1, idx + 1)
            st.rerun()
    with col3:
        if st.button("Finish & Score", type="primary"):
            st.session_state.stage = "results"
            st.rerun()

# --------------------------
# UI: Results
# --------------------------
if st.session_state.stage == "results":
    lens = st.session_state.lens
    qs = st.session_state.active_questions
    answers = st.session_state.answers

    overall, per_variable, scored_qs_sorted = compute_scores(qs, answers)

    st.subheader("Readout")
    st.write(lens_readout_intro(lens))

    st.metric("Overall Score (0–100)", f"{overall:.1f}", help="Weighted average of variable scores. Same math across lenses.")

    # Variable table
    st.write("### Variable Scores")
    for v in VARIABLE_WEIGHTS.keys():
        if v not in per_variable:
            continue
        info = per_variable[v]
        label = lens_translation(lens, v)
        st.write(
            f"- **{label}**: **{info['pct']:.1f}** ({info['zone']}) "
            f"— volatility **{info['volatility']:.0f}/100**"
        )

    # Strengths + Risks
    vars_present = [(v, per_variable[v]["pct"]) for v in per_variable]
    vars_present_sorted = sorted(vars_present, key=lambda x: x[1])

    if vars_present_sorted:
        lowest = vars_present_sorted[0][0]
        highest = vars_present_sorted[-1][0]

        st.write("### Where you are")
        st.write(f"- **Strongest area:** {lens_translation(lens, highest)} (**{per_variable[highest]['pct']:.1f}**)")

        st.write("### Where problems are arising")
        st.write(f"- **Primary risk area:** {lens_translation(lens, lowest)} (**{per_variable[lowest]['pct']:.1f}**, {per_variable[lowest]['zone']})")

        # Dominant distortions: lowest 5 questions overall, plus 3 from the lowest variable
        st.write("### Dominant distortions (lowest signals)")
        worst_overall = scored_qs_sorted[:5]
        for v, s, w, q, a in worst_overall:
            st.write(f"- {q['text']}  \n  ↳ scored **{s}/4** (weight {w})")

        st.write("### Smallest lever (best first adjustment)")
        # Pick the single most leveraged low question: among the lowest variable, choose lowest score then highest weight
        low_var_items = [t for t in scored_qs_sorted if t[0] == lowest]
        if low_var_items:
            lever = sorted(low_var_items, key=lambda t: (t[1], -t[2]))[0]
            v, s, w, q, a = lever
            st.write(f"**Do this first:** {q['text']}")
            st.caption(f"Why: it’s inside your lowest area ({lens_translation(lens, lowest)}) and carries high leverage (weight {w}).")

        st.write("### Areas that need adjustment to continue evaluation")
        # A simple next-path recommendation: drill into lowest variable + any other RED
        reds = [v for v in per_variable if per_variable[v]["zone"] == "RED"]
        yellows = [v for v in per_variable if per_variable[v]["zone"] == "YELLOW"]
        next_targets = []
        if lowest not in next_targets:
            next_targets.append(lowest)
        for v in reds:
            if v not in next_targets:
                next_targets.append(v)
        if len(next_targets) < 2:
            for v in yellows:
                if v not in next_targets:
                    next_targets.append(v)
                if len(next_targets) >= 2:
                    break

        st.write("- **Next focus targets:**")
        for v in next_targets[:3]:
            st.write(f"  - {lens_translation(lens, v)} ({per_variable[v]['pct']:.1f})")

    st.divider()
    st.write("### Export (copy/paste)")
    st.code(
        {
            "lens": lens,
            "overall": round(overall, 2),
            "variables": {v: round(per_variable[v]["pct"], 2) for v in per_variable},
            "answers": answers,
        },
        language="python"
    )

    colA, colB = st.columns([1,1])
    with colA:
        if st.button("Start a new run (same lens)"):
            # reshuffle and restart
            bank = QUESTION_BANK[lens][:]
            random.shuffle(bank)
            st.session_state.active_questions = bank[:25]
            st.session_state.q_order = [q["id"] for q in st.session_state.active_questions]
            st.session_state.idx = 0
            st.session_state.answers = {}
            st.session_state.stage = "questions"
            st.rerun()
    with colB:
        if st.button("Change lens"):
            reset_run()
            st.rerun()
