import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Melodian Records", layout="wide")

# Use the cleaner URL format
url = "https://docs.google.com/spreadsheets/d/1gyvI0dbvox31fCBAWkpxXTYGDmlL53Lyght3Yy1KkzQ/edit#gid=0"

st.title("🌐 Melodian Collaborative Registry")

# Establish connection
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Read data - specifying the worksheet can help avoid 404s
    data = conn.read(spreadsheet=url, worksheet="0") 
    data = data.dropna(how="all")

    with st.expander("➕ Add New Entry", expanded=True):
        with st.form("entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("First Name")
                family = st.selectbox("Family Members", options=[1, 2, 3, 4, 5])
            with col2:
                residence = st.text_input("Residence")
                course = st.selectbox("Course", ["Computer Science", "Data Science", "AI", "Business"])
            
            submit = st.form_submit_button("Save to Cloud")

    if submit and name and residence:
        new_row = pd.DataFrame([{"Name": name, "Family": family, "Residence": residence, "Course": course}])
        updated_df = pd.concat([data, new_row], ignore_index=True)
        conn.update(spreadsheet=url, data=updated_df)
        st.success("Successfully saved to Google Sheets!")
        st.rerun()

    if not data.empty:
        st.subheader("Current Database")
        st.table(data)

        if st.button("📄 Export to PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, "Student Registry Report", ln=True, align='C')
            pdf.ln(10)
            
            # Table Header
            pdf.set_font("Arial", 'B', 10)
            cols = ["Name", "Family", "Residence", "Course"]
            for col in cols:
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
        st.info("The database is currently empty. Add someone above!")

except Exception as e:
    st.error("🚨 Almost there! The app can't see the Sheet yet.")
    st.markdown("""
    **Please check these 3 things:**
    1. In Google Sheets, click **Share** -> Change to **Anyone with the link** -> Set to **Editor**.
    2. Make sure you have at least one row of headers in the sheet.
    3. Ensure `st-gsheets-connection` is in your `requirements.txt`.
    """)
    st.info(f"Technical Log: {e}")
