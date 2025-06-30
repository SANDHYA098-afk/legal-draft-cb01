import streamlit as st

# Set up the page
st.set_page_config(page_title="Legal Chat Assistant")

# Initialize session state variables
if "step" not in st.session_state:
    st.session_state.step = "start"
if "doc_type" not in st.session_state:
    st.session_state.doc_type = ""
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "custom_law" not in st.session_state:
    st.session_state.custom_law = ""

# Document types and related laws
doc_types = {
    "Non-Disclosure Agreement (NDA)": ["Indian Contract Act, 1872", "Information Technology Act, 2000"],
    "Lease Agreement": ["Rent Control Act, 1948", "Transfer of Property Act, 1882"],
    "Employment Contract": ["Industrial Disputes Act, 1947", "Shops and Establishments Act"],
    "IT Services Agreement": ["Information Technology Act, 2000"],
    "Freelance Work Contract": ["Copyright Act, 1957", "Indian Contract Act, 1872"]
}

st.title("📄 Legal Document Chat Assistant")

# Step-wise prompts and logic
if st.session_state.step == "start":
    st.write("👋 Welcome! What type of legal document do you want to draft?")
    for doc in doc_types:
        st.write(f"- {doc}")
    st.session_state.step = "doc_type"

elif st.session_state.step == "doc_type":
    user_input = st.text_input("Enter document type:")
    if user_input:
        matched_doc = None
        for doc in doc_types:
            if doc.lower() in user_input.lower():
                matched_doc = doc
                break
        if matched_doc:
            st.session_state.doc_type = matched_doc
            st.session_state.step = "party_a"
        else:
            st.error("Please enter a valid document type from the list above.")

elif st.session_state.step == "party_a":
    st.write("Enter Party A details (each on a new line):")
    st.markdown("*Full Name*  \nResidential Address  \nCity  \nState  \nOccupation  \nContact Number  \nEmail")
    party_a_input = st.text_area("Party A Details:")
    if party_a_input:
        lines = party_a_input.strip().split("\n")
        if len(lines) >= 6:
            st.session_state.answers["party_a"] = party_a_input.strip()
            st.session_state.step = "party_b"
        else:
            st.error("Please enter at least 6 lines for Party A.")

elif st.session_state.step == "party_b":
    st.write("Enter Party B details in the same format:")
    party_b_input = st.text_area("Party B Details:")
    if party_b_input:
        lines = party_b_input.strip().split("\n")
        if len(lines) >= 6:
            st.session_state.answers["party_b"] = party_b_input.strip()
            st.session_state.step = "law"
        else:
            st.error("Please enter at least 6 lines for Party B.")

elif st.session_state.step == "law":
    st.write("Select applicable law or type your own:")
    law_options = doc_types[st.session_state.doc_type] + ["Other"]
    selected_law = st.selectbox("Choose Law:", law_options)
    if selected_law == "Other":
        custom_law = st.text_input("Type your custom law:")
        if custom_law:
            st.session_state.answers["law"] = custom_law
            st.session_state.step = "done"
    else:
        st.session_state.answers["law"] = selected_law
        st.session_state.step = "done"

elif st.session_state.step == "done":
    st.write("✅ All details are collected.")
    if st.button("Generate Document"):
        st.session_state.step = "generate"

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
    st.markdown("---")
    st.markdown("### 📄 Document Preview")
    st.markdown(f"<pre style='white-space: pre-wrap; font-family: monospace;'>{draft.strip()}</pre>", unsafe_allow_html=True)
    st.download_button("⬇ Download Document", draft.strip(), file_name="legal_document.txt")
    st.success("Your document is ready!")
    st.session_state.step = "completed"

elif st.session_state.step == "completed":
    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
