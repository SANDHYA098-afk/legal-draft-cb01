import streamlit as st

# ---- CONFIGURATION ----
st.set_page_config(page_title="Legal Chat Assistant", layout="centered")

# ---- STATE INITIALIZATION ----
if "step" not in st.session_state: st.session_state.step = "start"
if "doc_type" not in st.session_state: st.session_state.doc_type = ""
if "answers" not in st.session_state: st.session_state.answers = {}
if "custom_law" not in st.session_state: st.session_state.custom_law = ""
if "draft" not in st.session_state: st.session_state.draft = ""

# ---- DOCUMENT TYPES ----
doc_types = {
    "Non-Disclosure Agreement (NDA)": ["Indian Contract Act, 1872", "Information Technology Act, 2000"],
    "Lease Agreement": ["Rent Control Act, 1948", "Transfer of Property Act, 1882"],
    "Employment Contract": ["Industrial Disputes Act, 1947", "Shops and Establishments Act"],
    "IT Services Agreement": ["Information Technology Act, 2000"],
    "Freelance Work Contract": ["Copyright Act, 1957", "Indian Contract Act, 1872"]
}

st.title("📄 Legal Document Chat Assistant")

# ---- STEP HANDLER ----

def step_start():
    st.info("👋 Welcome! Let's get started.")
    st.write("Choose the type of legal document you want to draft:")
    with st.form("doc_type_form"):
        doc = st.selectbox("Select Document Type", list(doc_types.keys()))
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.doc_type = doc
            st.session_state.step = "party_a"

def step_party_a():
    st.info("📝 Enter Party A's Details")
    with st.form("party_a_form"):
        party_a = st.text_area("Full Name\nAddress\nCity\nState\nOccupation\nPhone\nEmail", height=180)
        submitted = st.form_submit_button("Next")
        if submitted:
            lines = party_a.strip().split("\n")
            if len(lines) < 6:
                st.warning("Please provide at least 6 lines.")
            else:
                st.session_state.answers["party_a"] = party_a.strip()
                st.session_state.step = "party_b"

def step_party_b():
    st.info("📝 Enter Party B's Details")
    with st.form("party_b_form"):
        party_b = st.text_area("Full Name\nAddress\nCity\nState\nOccupation\nPhone\nEmail", height=180)
        submitted = st.form_submit_button("Next")
        if submitted:
            lines = party_b.strip().split("\n")
            if len(lines) < 6:
                st.warning("Please provide at least 6 lines.")
            else:
                st.session_state.answers["party_b"] = party_b.strip()
                st.session_state.step = "law"

def step_law():
    st.info("📚 Select or Enter Applicable Law")
    with st.form("law_form"):
        law_list = doc_types[st.session_state.doc_type] + ["Other"]
        law_choice = st.selectbox("Select Law", law_list)
        custom = ""
        if law_choice == "Other":
            custom = st.text_input("Enter your custom law")
        submitted = st.form_submit_button("Next")
        if submitted:
            final_law = custom if law_choice == "Other" else law_choice
            if not final_law.strip():
                st.warning("Please enter a valid law.")
            else:
                st.session_state.answers["law"] = final_law
                st.session_state.step = "confirm"

def step_confirm():
    st.success("✅ All details collected.")
    if st.button("Generate Document"):
        st.session_state.step = "generate"

def step_generate():
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
    st.session_state.draft = draft.strip()
    st.session_state.step = "final"

def step_final():
    st.markdown("---")
    st.subheader("📄 Your Document Preview")
    st.code(st.session_state.draft, language="text")
    st.download_button("⬇ Download as Text File", st.session_state.draft, file_name="legal_document.txt")
    st.success("🎉 Document is ready!")
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# ---- FLOW CONTROLLER ----
step_flow = {
    "start": step_start,
    "party_a": step_party_a,
    "party_b": step_party_b,
    "law": step_law,
    "confirm": step_confirm,
    "generate": step_generate,
    "final": step_final,
}

step_flow[st.session_state.step]()  # execute the current step
