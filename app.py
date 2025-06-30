import streamlit as st

st.set_page_config(page_title="Legal Document Assistant", page_icon="📄")

st.title("📄 Legal Document Drafting Assistant")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

questions = [
    "What type of legal document would you like to draft?",
    "Enter Party A's name:",
    "Enter Party B's name:",
    "Which jurisdiction should apply?",
    "What is the effective date?"
]

# Show questions one by one
if st.session_state.step < len(questions):
    question = questions[st.session_state.step]
    user_input = st.text_input(f"Q{st.session_state.step + 1}: {question}", key=f"input_{st.session_state.step}")

    if user_input:
        st.session_state.answers[f"q{st.session_state.step}"] = user_input
        st.session_state.step += 1
        st.experimental_rerun()
else:
    q = st.session_state.answers
    st.success("✅ Legal Document Generated Below:")
    st.markdown(f"""
    ### 📝 Drafted {q['q0'].upper()} Document

    This {q['q0']} is made between *{q['q1']}* and *{q['q2']}, effective from **{q['q4']}, governed by the laws of **{q['q3']}*.

    *Terms & Conditions:*
    - Both parties agree in good faith.
    - This agreement remains valid until mutually terminated.

    Note: This is an AI-generated draft for demonstration.
    """)

    if st.button("Reset"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.experimental_rerun()
