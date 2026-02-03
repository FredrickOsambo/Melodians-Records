import streamlit as st
from fpdf import FPDF

# App Title
st.set_page_config(page_title="Course Registration", page_icon="📝")
st.title("🎓 Student Information Portal")

# Sidebar Collaboration Note
st.sidebar.info("Collaborative Mode: Edit the code on GitHub to update this form.")

# Form Fields
with st.form("student_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        family_name = st.text_input("Family Name")
    with col2:
        residence = st.text_input("Residence / City")
        course = st.selectbox("Select Course", ["Computer Science", "Data Science", "AI", "Business"])
    
    submitted = st.form_submit_button("Generate PDF")

# PDF Generation Logic
if submitted:
    if not first_name or not family_name:
        st.error("Please fill in the required fields.")
    else:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Student Registration Details", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10) # Line break
        pdf.cell(200, 10, txt=f"First Name: {first_name}", ln=True)
        pdf.cell(200, 10, txt=f"Family Name: {family_name}", ln=True)
        pdf.cell(200, 10, txt=f"Residence: {residence}", ln=True)
        pdf.cell(200, 10, txt=f"Course: {course}", ln=True)
        
        # Output PDF to a string buffer
        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        st.success("✅ PDF Generated successfully!")
        st.download_button(
            label="📥 Download PDF",
            data=pdf_output,
            file_name=f"{first_name}_{family_name}_registration.pdf",
            mime="application/pdf"
        )