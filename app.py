import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from fpdf import FPDF

# App Setup
st.set_page_config(page_title="Melodian Registry", layout="centered")
st.title("📝 Simple Course Registry")

# Connection to Google Sheet
# Ensure you have set 'spreadsheet' in your Streamlit Secrets!
conn = st.connection("gsheets", type=GSheetsConnection)

# 1. Capture Data via Form
with st.form("input_form"):
    st.subheader("Add New Student")
    name = st.text_input("Full Name")
    family = st.selectbox("Family Number", options=[1, 2, 3, 4, 5])
    residence = st.text_input("Residence")
    course = st.selectbox("Course", ["Computer Science", "Data Science", "AI", "Business"])
    
    submit_button = st.form_submit_button("Submit & Save")

# 2. Logic to Save
if submit_button:
    if name and residence:
        # Read existing data
        existing_data = conn.read(ttl=0)
        
        # Create new entry
        new_entry = pd.DataFrame([{
            "Name": name,
            "Family": family,
            "Residence": residence,
            "Course": course
        }])
        
        # Combine and update
        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        conn.update(data=updated_data)
        st.success(f"Successfully saved {name} to the cloud!")
    else:
        st.warning("Please fill in all fields.")

# 3. View Data & Download PDF
st.divider()
st.subheader("Current Registry")
current_df = conn.read(ttl=0).dropna(how="all")
st.dataframe(current_df, use_container_width=True)

if not current_df.empty:
    if st.button("📄 Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Student Registration Report", ln=True, align='C')
        pdf.ln(10)
        
        # Table Headers
        pdf.set_font("Arial", 'B', 12)
        cols = ["Name", "Family", "Residence", "Course"]
        for col in cols:
            pdf.cell(45, 10, col, 1)
        pdf.ln()
        
        # Table Content
        pdf.set_font("Arial", size=10)
        for _, row in current_df.iterrows():
            for col in cols:
                pdf.cell(45, 10, str(row[col]), 1)
            pdf.ln()
            
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download PDF", pdf_output, "registry.pdf", "application/pdf")
