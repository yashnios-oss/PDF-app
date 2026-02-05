import streamlit as st
import tabula
import pandas as pd
from io import BytesIO
import tempfile
import os

# --- Page Config ---
st.set_page_config(page_title="PDF to Excel Converter", page_icon="📊")

# --- Title and Description ---
st.title("📊 PDF to Excel Converter")
st.write("""
Upload a PDF file containing tables, and this app will extract the data 
and convert it into a downloadable Excel file.
""")

st.markdown("---")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.info("File uploaded successfully! Processing...")

    # Create a temporary file to store the uploaded PDF
    # Tabula requires a file path, not just a bytes object
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    try:
        # --- PDF Processing (Extract Tables) ---
        # pages='all' extracts tables from all pages
        # multiple_tables=True handles pages with multiple distinct tables
        dfs = tabula.read_pdf(temp_pdf_path, pages='all', multiple_tables=True)

        if not dfs:
            st.error("No tables found in the PDF. Please ensure the PDF contains selectable text tables (not images).")
        else:
            st.success(f"Found {len(dfs)} table(s) in the document.")

            # --- Preview Section ---
            st.subheader("Preview Extracted Data")
            # Show the first few tables (limit to avoid UI clutter)
            for i, df in enumerate(dfs[:3]):
                st.write(f"**Table {i+1}**")
                st.dataframe(df)
            
            if len(dfs) > 3:
                st.info(f"...and {len(dfs) - 3} more table(s).")

            # --- Excel Conversion ---
            # Create an in-memory buffer for the Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, df in enumerate(dfs):
                    # Write each table to a separate sheet or combine them
                    # Here we write them to separate sheets named Table_1, Table_2, etc.
                    sheet_name = f"Table_{i+1}"
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
            
            output.seek(0)

            # --- Download Button ---
            st.download_button(
                label="📥 Download Excel File",
                data=output,
                file_name="converted_tables.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
    
    finally:
        # Cleanup: Remove the temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

else:
    st.info("Please upload a PDF file to begin.")
