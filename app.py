import streamlit as st
from io import StringIO

# Page configuration
st.set_page_config(page_title="Legal Document Assistant", page_icon="📄")

# Sidebar
with st.sidebar:
    st.title("⚖ Legal Drafting AI")
    st.markdown("""
Welcome to your legal assistant!  
Draft professional legal documents with ease.

*Made by:* Your Name  
[GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)
    """)

# Title
st.title("📄 Legal Document Drafting Assistant")
st.caption("Answer a few simple questions to generate a professional-looking legal agreement.")

# Initialize session
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Questions with friendly prompts
questions = [
    "First, what type of legal document would you like to draft? (e.g., NDA, lease agreement, contract)",
    "Great! Who is Party A? (Full name)",
    "And who is Party B? (Full name)",
    "Under which jurisdiction should this agreement be governed?",
    "Finally, from which date should this agreement become effective? (e.g., 01/07/2025)"
]

# Ask one question at a time
if st.session_state.step < len(questions):
    question = questions[st.session_state.step]
    st.markdown(f"*Q{st.session_state.step + 1}:* {question}")

    with st.form(key="input_form", clear_on_submit=True):
        user_input = st.text_input("Your answer:")
        submitted = st.form_submit_button("Submit")

        if submitted and user_input.strip():
            st.session_state.answers[f'q{st.session_state.step}'] = user_input.strip()
            st.session_state.step += 1
            st.experimental_rerun()

else:
    q = st.session_state.answers
    document = f"""
    📄 *DRAFTED {q['q0'].upper()} DOCUMENT*

    This {q['q0']} is made between *{q['q1']}* and *{q['q2']}*,  
    effective from *{q['q4']}, and governed by the laws of **{q['q3']}*.

    ---
    *TERMS & CONDITIONS*  
    • Both parties agree to the terms laid out in good faith.  
    • This agreement remains valid until mutually terminated or superseded.

    This is an AI-generated draft. Please consult a legal advisor before official use.
    """

    st.success("✅ Your Legal Document is Ready!")
    st.markdown(document)

    # Download as text file
    draft_file = StringIO(document)
    st.download_button(
        label="📥 Download Document as .txt",
        data=draft_file,
        file_name="legal_draft.txt",
        mime="text/plain"
    )

    # Reset
    if st.button("🔄 Start Over"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.experimental_rerun()
