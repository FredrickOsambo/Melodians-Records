import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Collaborative Registry", layout="wide")

# 1. Setup URL (Ensure it is in quotes!)
url = "https://docs.google.com/spreadsheets/d/1gyvI0dbvox31fCBAWkpxXTYGDmlL53Lyght3Yy1KkzQ/export?format=csv"

st.title("🌐 Live Collaborative Registry")

try:
    # 2. Connect to Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url, usecols=[0,1,2,3])
    data = data.dropna(how="all") # Remove empty rows

    # 3. Input Section
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
            new_row = pd.DataFrame([{"Name": name, "Family": family, "Residence": residence, "Course": course}])
            updated_df = pd.concat([data, new_row], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            st.success("Saved to Google Sheets!")
            st.rerun()

    # 4. Display & Management
    if not data.empty:
        st.subheader("Current Database")
        st.table(data)

        if st.button("📄 Export to PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, "Student Registry", ln=True, align='C')
            pdf.ln(10)
            
            # Table Headers
            pdf.set_font("Arial", 'B', 10)
            for col in ["Name", "Family", "Residence", "Course"]:
                pdf.cell(45, 10, col, 1)
            pdf.ln()

            # Table Rows
            pdf.set_font("Arial", size=10)
            for _, row in data.iterrows():
                pdf.cell(45, 10, str(row['Name']), 1)
                pdf.cell(45, 10, str(row['Family']), 1)
                pdf.cell(45, 10, str(row['Residence']), 1)
                pdf.cell(45, 10, str(row['Course']), 1)
                pdf.ln()

            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 Download PDF", pdf_bytes, "registry.pdf")
    else:
        st.info("The sheet is currently empty. Add the first entry above!")

except Exception as e:
    st.error("🚨 Connection Error!")
    st.write("Please ensure your Google Sheet is shared with 'Anyone with the link' as 'Editor'.")
    st.info(f"Technical details: {e}")
