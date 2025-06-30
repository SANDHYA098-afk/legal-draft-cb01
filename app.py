import streamlit as st 
import re

st.set_page_config(page_title="Legal Chat Assistant")

#Initialize session state

if "step" not in st.session_state: st.session_state.step = "start" if "doc_type" not in st.session_state: st.session_state.doc_type = "" if "answers" not in st.session_state: st.session_state.answers = {} if "last_input" not in st.session_state: st.session_state.last_input = ""

Document types and laws

doc_types = { "Non-Disclosure Agreement (NDA)": ["Indian Contract Act, 1872", "Information Technology Act, 2000"], "Lease Agreement": ["Rent Control Act, 1948", "Transfer of Property Act, 1882"], "Employment Contract": ["Industrial Disputes Act, 1947", "Shops and Establishments Act"], "IT Services Agreement": ["Information Technology Act, 2000"], "Freelance Work Contract": ["Copyright Act, 1957", "Indian Contract Act, 1872"] }

st.title("Legal Document Chat Assistant")

Chat interaction

user_input = st.text_input("You:")

if user_input: st.session_state.last_input = user_input.lower()

# Handle first step
if st.session_state.step == "start":
    st.write("Assistant: Welcome! What type of legal document do you want to draft?")
    for doc in doc_types:
        st.write(f"- {doc}")
    st.session_state.step = "doc_type"

elif st.session_state.step == "doc_type":
    for doc in doc_types:
        if doc.lower() in st.session_state.last_input:
            st.session_state.doc_type = doc
            st.session_state.step = "party_a"
            st.write(f"Assistant: Great. Please enter the details of Party A in the following format:\n\n"
                     "Full Name\nResidential Address\nCity\nState\nOccupation (e.g. Self-employed, Business, Office)\nContact Number\nEmail")
            break

elif st.session_state.step == "party_a":
    st.session_state.answers["party_a"] = st.session_state.last_input.strip()
    st.session_state.step = "party_b"
    st.write("Assistant: Now, enter the details of Party B in the same format:")

elif st.session_state.step == "party_b":
    st.session_state.answers["party_b"] = st.session_state.last_input.strip()
    st.session_state.step = "law"
    st.write("Assistant: Please select the applicable law from the options below or type your own:")
    for law in doc_types[st.session_state.doc_type]:
        st.write(f"- {law}")
    st.write("Or type your custom law.")

elif st.session_state.step == "law":
    st.session_state.answers["law"] = st.session_state.last_input.strip()
    st.session_state.step = "done"
    st.write("Assistant: Thank you. Hope all the details are entered correctly. If you'd like to change anything, type the word 'change'. Otherwise, your document will be prepared now.")

elif st.session_state.step == "done":
    if "change" in st.session_state.last_input:
        st.write("Assistant: What would you like to change? (e.g., 'change party a', 'change law')")
        st.session_state.step = "change_pending"
    else:
        st.write("Assistant: Drafting your document now...")
        st.session_state.step = "generate"

elif st.session_state.step == "change_pending":
    if "party a" in st.session_state.last_input:
        st.write("Assistant: Please re-enter Party A details:")
        st.session_state.step = "party_a"
    elif "party b" in st.session_state.last_input:
        st.write("Assistant: Please re-enter Party B details:")
        st.session_state.step = "party_b"
    elif "law" in st.session_state.last_input:
        st.write("Assistant: Please re-enter law selection:")
        st.session_state.step = "law"
    else:
        st.write("Assistant: Sorry, I didn't understand. Please specify what to change (e.g., 'change party a').")

elif st.session_state.step == "generate":
    a = st.session_state.answers
    doc_type = st.session_state.doc_type.upper()
    draft = f"""
    LEGAL DOCUMENT: {doc_type}

    THIS AGREEMENT is made between the following parties:

    PARTY A:
    {a['party_a']}

    AND

    PARTY B:
    {a['party_b']}

    This agreement is governed by: {a['law']}

    Both parties agree to abide by the terms and conditions outlined in this document.

    [Disclaimer: This is an AI-generated sample draft. Review with legal counsel before use.]
    """

    st.session_state.draft = draft

    # Show clean printable version
    st.markdown("---")
    st.markdown("### Document Preview")
    st.markdown(
        f"""
        <div style='background: #fff; padding: 20px; border: 1px solid #ddd; font-family: Arial, sans-serif;'>
            <h2 style='text-align: center;'>LEGAL DOCUMENT: {doc_type}</h2>
            <pre style='white-space: pre-wrap; font-size: 14px;'>{draft.strip()}</pre>
        </div>
        <script>
            function printDoc() {{
                window.print();
            }}
        </script>
        <button onclick="printDoc()">Print / Save as PDF</button>
        """,
        unsafe_allow_html=True
    )
    st.session_state.step = "completed"

elif st.session_state.step == "completed": st.write("Assistant: Your document is ready! You may restart the app to create a new one.")
