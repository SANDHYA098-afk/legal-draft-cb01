import streamlit as st import datetime import requests

st.set_page_config(page_title="Legal Chat Assistant")

Initialize session state

if "step" not in st.session_state: st.session_state.step = "start" if "doc_type" not in st.session_state: st.session_state.doc_type = "" if "answers" not in st.session_state: st.session_state.answers = {}

st.title("🧾 Legal Document Drafting Assistant") st.markdown("This assistant helps you generate legal documents and get legal term clarifications.")

Step 1: Ask for the document type

if st.session_state.step == "start": doc_type = st.text_input("What type of legal document do you want to draft? (e.g., NDA, Lease Agreement, Contract)") if doc_type: st.session_state.doc_type = doc_type st.session_state.step = "collect_info"

Step 2: Collect required information

elif st.session_state.step == "collect_info": answers = st.session_state.answers

if "party_a" not in answers:
    answers["party_a"] = st.text_input("Enter the name of Party A")
elif "party_b" not in answers:
    answers["party_b"] = st.text_input("Enter the name of Party B")
elif "effective_date" not in answers:
    answers["effective_date"] = st.date_input("Enter the effective date")
elif "duration" not in answers:
    answers["duration"] = st.number_input("Enter the duration of the agreement in years", min_value=1)
elif "jurisdiction" not in answers:
    answers["jurisdiction"] = st.text_input("Enter the governing jurisdiction (e.g., State/Country)")
else:
    st.session_state.step = "generate"

Step 3: Generate and show the document

elif st.session_state.step == "generate": a = st.session_state.answers doc = f""" This {st.session_state.doc_type} is made and entered into on {a['effective_date'].strftime('%B %d, %Y')} by and between {a['party_a']} and {a['party_b']}.

1. Purpose: The parties agree to the terms and conditions of this {st.session_state.doc_type} to facilitate a professional relationship.


2. Term: This agreement shall remain in effect for {a['duration']} years from the effective date.


3. Jurisdiction: This agreement shall be governed by and construed in accordance with the laws of {a['jurisdiction']}.



IN WITNESS WHEREOF, the parties have executed this agreement as of the date written above.


---

{a['party_a']}                      {a['party_b']} """ st.subheader("📝 Drafted Legal Document") st.text_area("Preview:", value=doc, height=400) st.download_button("📄 Download as Text", data=doc, file_name="Drafted_Legal_Document.txt")

Module 2: Legal Q&A Section

st.markdown("---") st.subheader("❓ Ask a Legal Question (Canada)") user_query = st.text_input("Enter your question about a legal term or concept:")

def fetch_legal_info(query): # Simulated API call - you can replace this with real CanLII or legal info search API simulated_responses = { "void and voidable contract": { "answer": "A void contract is invalid from the beginning, while a voidable contract is valid until one party chooses to void it.", "source": "https://www.canlii.org/en/ca/laws.html" }, "consideration in contract": { "answer": "Consideration is something of value exchanged between parties, essential for a valid contract.", "source": "https://www.canlii.org/en/ca/laws.html" } } for key in simulated_responses: if key in query.lower(): return simulated_responses[key] return { "answer": "Sorry, I couldn’t find a legal answer for that. Please refine your query or try again later.", "source": "https://www.canlii.org" }

if user_query: result = fetch_legal_info(user_query) st.markdown(f"Answer: {result['answer']}") st.markdown(f"📚 View Source")
