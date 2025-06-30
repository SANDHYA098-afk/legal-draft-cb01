import streamlit as st
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Legal Drafting AI", page_icon="📄")

# Sidebar
with st.sidebar:
    st.title("⚖ Legal Drafting Assistant")
    st.markdown("""
Draft professional legal documents easily!

*Created by:* Your Name  
[GitHub](https://github.com/yourusername)  
[LinkedIn](https://linkedin.com/in/yourprofile)
""")

st.title("📑 AI-Powered Legal Document Generator")

# Document Types
doc_types = {
    "Non-Disclosure Agreement (NDA)": [
        "Indian Contract Act, 1872",
        "Information Technology Act, 2000"
    ],
    "Lease Agreement": [
        "Rent Control Act, 1948",
        "Transfer of Property Act, 1882"
    ],
    "Employment Contract": [
        "Industrial Disputes Act, 1947",
        "Shops and Establishments Act"
    ],
    "IT Services Agreement": [
        "Information Technology Act, 2000",
        "Indian Contract Act, 1872"
    ],
    "Education Consultancy Agreement": [
        "Indian Contract Act, 1872",
        "Education Act, 2009"
    ],
    "Freelance Work Contract": [
        "Copyright Act, 1957",
        "Indian Contract Act, 1872"
    ],
    "Research Collaboration MOU": [
        "IPR Policy Guidelines",
        "Science & Tech Policy"
    ],
    "Partnership Deed": [
        "Partnership Act, 1932"
    ]
}

# Form
with st.form("legal_form"):
    st.subheader("Step 1: Choose Document Type")
    doc_type = st.selectbox("Select the type of legal document", list(doc_types.keys()))

    st.subheader("Step 2: Enter Party A's Details")
    a_name = st.text_input("Full Name (Party A)")
    a_addr = st.text_input("Address (Party A)")
    a_phone = st.text_input("Phone Number (Party A)")
    a_email = st.text_input("Email (Party A, optional)")

    st.subheader("Step 3: Enter Party B's Details")
    b_name = st.text_input("Full Name (Party B)")
    b_addr = st.text_input("Address (Party B)")
    b_phone = st.text_input("Phone Number (Party B)")
    b_email = st.text_input("Email (Party B, optional)")

    st.subheader("Step 4: Select Governing Law")
    law = st.selectbox("Applicable Law / Jurisdiction", doc_types[doc_type] + ["Other"])
    if law == "Other":
        law = st.text_input("Enter your own jurisdiction/law")

    st.subheader("Step 5: Agreement Effective Date")
    effective_date = st.date_input("Choose effective date", value=datetime.today())

    submitted = st.form_submit_button("📄 Generate Document")

# On Submit
if submitted:
    # Drafting the document text
    content = f"""
    {doc_type.upper()}

    This agreement is entered into by and between:

    PARTY A:
    Name: {a_name}
    Address: {a_addr}
    Phone: {a_phone}
    Email: {a_email if a_email else 'N/A'}

    AND

    PARTY B:
    Name: {b_name}
    Address: {b_addr}
    Phone: {b_phone}
    Email: {b_email if b_email else 'N/A'}

    Effective Date: {effective_date.strftime('%d %B %Y')}
    Governing Law: {law}

    TERMS:
    • This {doc_type.lower()} is governed under the laws of {law}.
    • Both parties agree to abide by the terms in good faith.
    • This agreement remains valid unless terminated in writing by either party.

    NOTE: This is an AI-generated draft. Please consult a legal expert before official use.
    """

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line.strip())

    # Convert to bytes
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    st.success("✅ Document successfully generated!")

    # Show preview (optional)
    st.text_area("📃 Document Preview", content, height=300)

    # Download button
    st.download_button(
        label="📥 Download as PDF",
        data=pdf_output,
        file_name="legal_document.pdf",
        mime="application/pdf"
    )
