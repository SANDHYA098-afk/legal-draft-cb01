import streamlit as st from fpdf import FPDF from io import BytesIO import re

st.set_page_config(page_title="Legal Chatbot Assistant", page_icon="📄")

Initialize session state

if "step" not in st.session_state: st.session_state.step = "start" if "doc_type" not in st.session_state: st.session_state.doc_type = "" if "answers" not in st.session_state: st.session_state.answers = {} if "edit" not in st.session_state: st.session_state.edit = False

Document types and laws

doc_types = { "Non-Disclosure Agreement (NDA)": ["Indian Contract Act, 1872", "Information Technology Act, 2000"], "Lease Agreement": ["Rent Control Act, 1948", "Transfer of Property Act, 1882"], "Employment Contract": ["Industrial Disputes Act, 1947", "Shops and Establishments Act"], "IT Services Agreement": ["Information Technology Act, 2000"], "Freelance Work Contract": ["Copyright Act, 1957", "Indian Contract Act, 1872"] }

st.title("👋 Legal Document Chat Assistant")

Start conversation

if st.session_state.step == "start": st.markdown("Hi! I'm your legal assistant 🤖. Let's draft your legal document.") doc_choice = st.selectbox("Which type of document would you like to draft?", list(doc_types.keys())) if st.button("Next"): st.session_state.doc_type = doc_choice st.session_state.step = "party_a"

Party A info

elif st.session_state.step == "party_a": st.subheader("Enter Party A's Details") a_name = st.text_input("Full Name", st.session_state.answers.get("a_name", "")) a_addr = st.text_input("Address", st.session_state.answers.get("a_addr", "")) a_city = st.text_input("City", st.session_state.answers.get("a_city", "")) a_state = st.text_input("State", st.session_state.answers.get("a_state", "")) a_country = "India" a_phone = st.text_input("Phone Number", st.session_state.answers.get("a_phone", "")) a_email = st.text_input("Email", st.session_state.answers.get("a_email", "")) if st.button("Next"): st.session_state.answers.update({ "a_name": a_name, "a_addr": a_addr, "a_city": a_city, "a_state": a_state, "a_country": a_country, "a_phone": a_phone, "a_email": a_email }) st.session_state.step = "party_b"

Party B info

elif st.session_state.step == "party_b": st.subheader("Enter Party B's Details") b_name = st.text_input("Full Name", st.session_state.answers.get("b_name", "")) b_addr = st.text_input("Address", st.session_state.answers.get("b_addr", "")) b_city = st.text_input("City", st.session_state.answers.get("b_city", "")) b_state = st.text_input("State", st.session_state.answers.get("b_state", "")) b_country = "India" b_phone = st.text_input("Phone Number", st.session_state.answers.get("b_phone", "")) b_email = st.text_input("Email", st.session_state.answers.get("b_email", "")) if st.button("Next"): st.session_state.answers.update({ "b_name": b_name, "b_addr": b_addr, "b_city": b_city, "b_state": b_state, "b_country": b_country, "b_phone": b_phone, "b_email": b_email }) st.session_state.step = "law"

Choose law

elif st.session_state.step == "law": st.subheader("Choose Governing Law") options = doc_types[st.session_state.doc_type] + ["Other"] selected = st.selectbox("Select applicable law", options) if selected == "Other": selected = st.text_input("Enter custom law", st.session_state.answers.get("law", "")) if st.button("Next"): st.session_state.answers["law"] = selected st.session_state.step = "confirm"

Confirm and allow edit

elif st.session_state.step == "confirm": st.subheader("Please confirm your details") for key, val in st.session_state.answers.items(): st.write(f"{key.replace('_', ' ').title()}: {val}") if st.button("Edit Details"): st.session_state.step = "party_a" elif st.button("Looks Good, Draft the Document"): st.session_state.step = "draft"

Draft and generate PDF

elif st.session_state.step == "draft": a = st.session_state.answers doc_type = st.session_state.doc_type.upper() draft = f""" LEGAL DOCUMENT: {doc_type}

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
This {st.session_state.doc_type.lower()} is governed under the above jurisdiction.
Both parties agree to honor and abide by the terms stated herein.

Disclaimer: This is an AI-generated draft document for educational/demo purposes only.
"""

st.success("✅ Your legal document has been drafted:")
st.text_area("📄 Document Preview", draft.strip(), height=400)

if st.button("📥 Generate PDF"):
    clean_text = re.sub(r"[^\x00-\x7F]+", " ", draft)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, f"LEGAL DOCUMENT: {doc_type}")
    pdf.set_font("Arial", size=12)
    for line in clean_text.split('\n'):
        pdf.multi_cell(0, 10, line.strip())

    pdf_out = BytesIO()
    pdf.output(pdf_out)
    pdf_out.seek(0)

    st.download_button(
        label="⬇ Download PDF",
        data=pdf_out,
        file_name="legal_document.pdf",
        mime="application/pdf"
    )
