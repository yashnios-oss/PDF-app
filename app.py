import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.title("PDF to Excel Converter")

uploaded_file = st.file_uploader("Upload your PDF here", type="pdf")

if uploaded_file is not None:
    try:
        # Open the PDF
        with pdfplumber.open(uploaded_file) as pdf:
            all_data = []
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    # Convert table to a list of data
                    df = pd.DataFrame(table)
                    all_data.append(df)
            
            if all_data:
                # Merge all tables into one
                final_df = pd.concat(all_data, ignore_index=True)
                
                # Show a preview so we know it worked!
                st.write("### Preview of extracted data:")
                st.dataframe(final_df)

                # Prepare Excel file in memory
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False)
                
                # Download button
                st.download_button(
                    label="Download Excel File",
                    data=buffer.getvalue(),
                    file_name="converted_pdf.xlsx",
                    mime="application/vnd.ms-excel"
                )
            else:
                st.error("We found the PDF, but couldn't find any clear tables inside.")
    except Exception as e:
        st.error(f"Error logic: {e}")
