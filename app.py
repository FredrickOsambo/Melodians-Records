import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Batch Registration", layout="wide")

# 1. Initialize Session State to store multiple entries
if 'student_list' not in st.session_state:
    st.session_state.student_list = []

st.title("👥 Multi-Student Data Collection")

# 2. Input Section
with st.expander("➕ Add New Entry", expanded=True):
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            family_size = st.selectbox("Family Members", options=[1, 2, 3, 4, 5])
        with col2:
            residence = st.text_input("Residence")
            course = st.selectbox("Course", ["Computer Science", "Data Science", "AI", "Business"])
        
        add_person = st.form_submit_button("Add to List")

# 3. Logic to add data to the session list
if add_person:
    if first_name and residence:
        new_entry = {
            "First Name": first_name,
            "Family": family_size,
            "Residence": residence,
            "Course": course
        }
        st.session_state.student_list.append(new_entry)
        st.toast(f"Added {first_name}!")
    else:
        st.error("Please fill in Name and Residence.")

# 4. Display the Table
if st.session_state.student_list:
    st.subheader("Current Registry")
    df = pd.DataFrame(st.session_state.student_list)
    st.table(df) # Shows a clean, non-editable table

    if st.button("🗑️ Clear List"):
        st.session_state.student_list = []
        st.rerun()

    # 5. PDF Generation (Table Format)
    if st.button("📄 Export All to PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Student Collection Report", ln=True, align='C')
        pdf.ln(10)

        # Table Header
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Name", 1)
        pdf.cell(30, 10, "Family", 1)
        pdf.cell(60, 10, "Residence", 1)
        pdf.cell(60, 10, "Course", 1, ln=True)

        # Table Rows
        pdf.set_font("Arial", size=10)
        for person in st.session_state.student_list:
            pdf.cell(40, 10, person["First Name"], 1)
            pdf.cell(30, 10, str(person["Family"]), 1)
            pdf.cell(60, 10, person["Residence"], 1)
            pdf.cell(60, 10, person["Course"], 1, ln=True)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="📥 Download PDF Table",
            data=pdf_output,
            file_name="student_registry.pdf",
            mime="application/pdf"
        )
else:
    st.info("No entries yet. Add someone above!")
