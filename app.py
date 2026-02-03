import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Collaborative Registry", layout="wide")

# 1. Connect to Google Sheets
# You will need to add your Sheet URL in the Streamlit Secrets or sidebar for now
url = "https://docs.google.com/spreadsheets/d/1gyvI0dbvox31fCBAWkpxXTYGDmlL53lYght3Yy1KkzQ/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data
data = conn.read(spreadsheet=url, usecols=[0,1,2,3])
data = data.dropna(how="all") # Clean empty rows

st.title("🌐 Live Collaborative Registry")
st.info("Data is saved instantly to Google Sheets. All users see the same list.")

# 2. Input Section
with st.expander("➕ Add New Entry"):
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("First Name")
            family = st.selectbox("Family Members", options=[1, 2, 3, 4, 5])
        with col2:
            residence = st.text_input("Residence")
            course = st.selectbox("Course", ["Computer Science", "Data Science", "AI", "Business"])
        
        submit = st.form_submit_button("Save to Cloud")

if submit:
    if name and residence:
        # Create new row
        new_row = pd.DataFrame([{
            "Name": name,
            "Family": family,
            "Residence": residence,
            "Course": course
        }])
        # Append to existing data and update sheet
        updated_df = pd.concat([data, new_row], ignore_index=True)
        conn.update(spreadsheet=url, data=updated_df)
        st.success("Saved to Cloud!")
        st.rerun()

# 3. Display Data
if not data.empty:
    st.subheader("Current Database")
    st.table(data)

    # 4. Delete Specific Row
    row_to_del = st.number_input("Row to delete", min_value=1, max_value=len(data), step=1)
    if st.button("🗑️ Delete Entry"):
        data = data.drop(data.index[int(row_to_del) - 1])
        conn.update(spreadsheet=url, data=data)
        st.rerun()

    # 5. PDF Generation
    if st.button("📄 Export Cloud Data to PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Shared Registry Report", ln=True, align='C')
        pdf.ln(10)
        
        # Header
        pdf.set_font("Arial", 'B', 10)
        cols = ["Name", "Family", "Residence", "Course"]
        for col in cols:
            pdf.cell(45, 10, col, 1)
        pdf.ln()

        # Data rows
        pdf.set_font("Arial", size=10)
        for _, row in data.iterrows():
            pdf.cell(45, 10, str(row['Name']), 1)
            pdf.cell(45, 10, str(row['Family']), 1)
            pdf.cell(45, 10, str(row['Residence']), 1)
            pdf.cell(45, 10, str(row['Course']), 1)
            pdf.ln()

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        st.download_button("📥 Download Cloud PDF", pdf_bytes, "cloud_registry.pdf")


