import streamlit as st from fpdf import FPDF from io import BytesIO

Set page config

st.set_page_config(page_title="Legal Chatbot Assistant", page_icon="📄")

Session init

if "step" not in st.session_state: st.session_state.step = "start" if "doc_type" not in st.session_state: st.session_state.doc_type = "" if "answers" not in st.session_state: st.session_state.answers = {}

Document types and laws

doc_types = { "Non-Disclosure Agreement (NDA)": ["Indian Contract Act, 1872", "Information Technology Act, 2000"], "Lease Agreement": ["Rent Control Act, 1948", "Transfer of Property Act, 1882"], "Employment Contract": ["Industrial Disputes Act, 1947", "Shops and Establishments Act"], "IT Services Agreement": ["Information Technology Act, 2000"], "Freelance Work Contract": ["Copyright Act, 1957", "Indian Contract Act, 1872"] }

st.title("Legal Document Chat Assistant")

Start conversation

if st.session_state.step == "start": st.markdown("Hello! I'm your Legal Drafting Assistant 🫠\n\nLet's get started with drafting your legal document.") doc_choice = st.selectbox("What type of document would you like to draft?", list(doc_types.keys())) if st.button("Next"): st.session_state.doc_type = doc_choice st.session_state.step = "party_a" st.experimental_rerun()

Party A info

elif st.session_state.step == "party_a": st.subheader("Enter Party A's Details") a_name = st.text_input("Full Name") a_addr = st.text_input("Residential Address") a_city = st.text_input("City") a_state = st.text_input("State") a_country = "India" a_phone = st.text_input("Contact Number") a_email = st.text_input("Email") if st.button("Next"): st.session_state.answers.update({ "a_name": a_name, "a_addr": a_addr, "a_city": a_city, "a_state": a_state, "a_country": a_country, "a_phone": a_phone, "a_email": a_email }) st.session_state.step = "party_b" st.experimental_rerun()

Party B info

elif st.session_state.step == "party_b": st.subheader("Enter Party B's Details") b_name = st.text_input("Full Name") b_addr = st.text_input("Residential Address") b_city = st.text_input("City") b_state = st.text_input("State") b_country = "India" b_phone = st.text_input("Contact Number") b_email = st.text_input("Email") if st.button("Next"): st.session_state.answers.update({ "b_name": b_name, "b_addr": b_addr, "b_city": b_city, "b_state": b_state, "b_country": b_country, "b_phone": b_phone, "b_email": b_email }) st.session_state.step = "law" st.experimental_rerun()

Choose law

elif st.session_state.step == "law": st.subheader("Choose Governing Law") law_choice = st.selectbox("Select applicable law", doc_types[st.session_state.doc_type] + ["Other"]) if law_choice == "Other": law_choice = st.text_input("Enter your custom law") if st.button("Next"): st.session_state.answers["law"] = law_choice st.session_state.step = "confirm" st.experimental_rerun()

Confirm

elif st.session_state.step == "confirm": st.subheader("Please confirm your details") for k, v in st.session_state.answers.items(): st.write(f"{k.replace('_', ' ').title()}: {v}") if st.button("Looks Good, Draft the Document"): st.session_state.step = "draft" st.experimental_rerun()

Draft and ask for PDF

elif st.session_state.step == "draft": a = st.session_state.answers draft = f""" LEGAL DOCUMENT: {st.session_state.doc_type.upper()}

This agreement is made between:

PARTY A:
Name: {a['a_name']}
Address: {a['a_addr']}, {a['a_city']}, {a['a_state']}, {a['a_country']}
Phone: {a['a_phone']}, Email: {a['a_email']}

AND

PARTY B:
Name: {a['b_name']}
Address: {a['b_addr']}, {a['b_city']}, {a['b_state']}, {a['b_country']}
Phone: {a['b_phone']}, Email: {a['b_email']}

Governing Law: {a['law']}

Terms:
This {st.session_state.doc_type.lower()} is governed under the above jurisdiction. Parties agree to honor terms.

Disclaimer: This is an AI-generated draft.
"""
st.success("Here is your drafted document:")
st.text_area("Drafted Legal Document", draft, height=350)

if st.button("📄 Generate PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, f"LEGAL DOCUMENT: {st.session_state.doc_type.upper()}")
    pdf.set_font("Arial", size=12)
    for line in draft.split('\n'):
        pdf.multi_cell(0, 10, line.strip())
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    st.download_button(
        label="📅 Download PDF",
        data=pdf_output,
        file_name="legal_document.pdf",
        mime="application/pdf"
    )
