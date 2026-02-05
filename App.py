import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.write("Upload a PDF with tables and download them as an Excel file.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            all_tables = []
            
            # 2. Extracting Tables
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)
            
            if all_tables:
                # Combine all tables into one DataFrame
                final_df = pd.concat(all_tables, ignore_index=True)
                
                st.success(f"Successfully extracted {len(all_tables)} tables!")
                st.dataframe(final_df.head()) # Preview the data
                
                # 3. Convert to Excel (Memory Buffer)
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='Sheet1')
                
                # 4. Download Button
                st.download_button(
                    label="📥 Download Excel File",
                    data=output.getvalue(),
                    file_name="converted_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.warning("No tables found in this PDF.")
                
    except Exception as e:
        st.error(f"An error occurred: {e}")
