"""
Universal Question Bank — v1
Questions are domain-agnostic.
They capture variables, not feelings.
"""

QUESTION_BANK = [
    # -------- BASELINE STABILITY --------
    {
        "id": "base_01",
        "text": "How many days this week did you wake up already feeling behind?",
        "variable": "Baseline Stability",
        "phase": 1,
        "weight": 1.0,
    },
    {
        "id": "base_02",
        "text": "How often does a single unexpected issue destabilize your entire day?",
        "variable": "Baseline Stability",
        "phase": 1,
        "weight": 1.1,
    },
    {
        "id": "base_03",
        "text": "How predictable are your days from start to finish?",
        "variable": "Baseline Stability",
        "phase": 1,
        "weight": 0.9,
    },
    {
        "id": "base_04",
        "text": "How often do you feel like you are operating without a buffer?",
        "variable": "Baseline Stability",
        "phase": 1,
        "weight": 1.1,
    },

    # -------- LOAD / CAPACITY --------
    {
        "id": "load_01",
        "text": "How often do you feel drained before the main part of your day even begins?",
        "variable": "Load",
        "phase": 1,
        "weight": 1.2,
    },
    {
        "id": "load_02",
        "text": "How often do you carry pressure without a clear source?",
        "variable": "Load",
        "phase": 1,
        "weight": 1.2,
    },
    {
        "id": "load_03",
        "text": "How often do you delay rest because it feels unsafe or irresponsible?",
        "variable": "Load",
        "phase": 2,
        "weight": 1.3,
    },
    {
        "id": "load_04",
        "text": "How often do you feel alert but unable to act?",
        "variable": "Load",
        "phase": 2,
        "weight": 1.3,
    },
    {
        "id": "load_05",
        "text": "How often does your body signal exhaustion before your mind agrees?",
        "variable": "Load",
        "phase": 2,
        "weight": 1.2,
    },

    # -------- SIGNAL CLARITY --------
    {
        "id": "signal_01",
        "text": "How often are you unsure whether what you’re doing is actually helping?",
        "variable": "Signal Clarity",
        "phase": 1,
        "weight": 1.1,
    },
    {
        "id": "signal_02",
        "text": "How often do you change behavior without knowing what caused the last outcome?",
        "variable": "Signal Clarity",
        "phase": 2,
        "weight": 1.2,
    },
    {
        "id": "signal_03",
        "text": "How often does silence feel like feedback?",
        "variable": "Signal Clarity",
        "phase": 2,
        "weight": 1.3,
    },

    # -------- FEEDBACK SAFETY --------
    {
        "id": "feedback_01",
        "text": "How often do you avoid speaking up because it will create more work than relief?",
        "variable": "Feedback Safety",
        "phase": 1,
        "weight": 1.2,
    },
    {
        "id": "feedback_02",
        "text": "How often do issues get addressed only after they become unavoidable?",
        "variable": "Feedback Safety",
        "phase": 2,
        "weight": 1.3,
    },
    {
        "id": "feedback_03",
        "text": "How often do things smooth over without actually changing?",
        "variable": "Feedback Safety",
        "phase": 2,
        "weight": 1.2,
    },

    # -------- INCENTIVES --------
    {
        "id": "incentive_01",
        "text": "How often are you rewarded for endurance rather than improvement?",
        "variable": "Incentives",
        "phase": 1,
        "weight": 1.2,
    },
    {
        "id": "incentive_02",
        "text": "How often do short-term fixes undermine longer-term outcomes?",
        "variable": "Incentives",
        "phase": 2,
        "weight": 1.3,
    },

    # -------- CONSTRAINTS --------
    {
        "id": "constraint_01",
        "text": "How many of your current limits feel non-negotiable?",
        "variable": "Constraints",
        "phase": 1,
        "weight": 1.2,
    },
    {
        "id": "constraint_02",
        "text": "How often do plans fail because they ignore one obvious constraint?",
        "variable": "Constraints",
        "phase": 2,
        "weight": 1.3,
    },

    # -------- TRAJECTORY / DRIFT --------
    {
        "id": "drift_01",
        "text": "How often do weeks blur together without a sense of direction?",
        "variable": "Trajectory",
        "phase": 1,
        "weight": 1.2,
    },
    {
        "id": "drift_02",
        "text": "How often does effort result in continuation rather than relief?",
        "variable": "Trajectory",
        "phase": 2,
        "weight": 1.3,
    },
    {
        "id": "drift_03",
        "text": "How often do you feel like you are maintaining position instead of changing it?",
        "variable": "Trajectory",
        "phase": 2,
        "weight": 1.4,
    },
]
