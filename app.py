import streamlit as st
from src.question_bank import QUESTION_BANK
from src.engine import evaluate

st.set_page_config(page_title="Mirror Without Light", layout="centered")

st.title("Mirror Without Light — Diagnostic")
st.caption("This tool decodes feedback. It does not judge intent.")

domain = st.selectbox(
    "Choose a lens",
    ["Relationship", "Financial", "Life Path"]
)

st.divider()

responses = {}

for q in QUESTION_BANK:
    with st.expander(q["variable"], expanded=False):
        val = st.slider(
            q["text"],
            0, 4, 2,
            key=q["id"]
        )
        responses[q["id"]] = (q, val)

if st.button("Decode"):
    formatted = {qid: score for qid, (q, score) in responses.items()}
    result = evaluate(
        {q: score for (_, (q, score)) in responses.items()},
        domain
    )

    st.header("Result")
    st.metric("Risk Level", result["risk"])

    st.subheader("Missing Variable")
    st.write(result["missing_variable"])

    st.subheader("How the Signal is Distorted")
    st.write(result["distortion"])

    st.subheader("Smallest Lever That Changes Trajectory")
    st.write(result["lever"])

    st.subheader("Primary Drivers")
    for name, value in result["drivers"]:
        st.write(f"- {name}: {value:.2f}")
