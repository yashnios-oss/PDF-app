import streamlit as st
import pdfplumber
import pandas as pd
import io

st.title("PDF to Excel Converter")

st.write("Upload a PDF file containing tables and convert it to Excel.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_tables_from_pdf(pdf_file):
    tables = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page_number, page in enumerate(pdf.pages):
            extracted_tables = page.extract_tables()
            
            for table in extracted_tables:
                if table:
                    df = pd.DataFrame(table)
                    
                    # Use first row as header if possible
                    df.columns = df.iloc[0]
                    df = df[1:]
                    
                    df["Page"] = page_number + 1
                    tables.append(df)
    
    return tables


if uploaded_file is not None:
    
    with st.spinner("Extracting tables from PDF..."):
        tables = extract_tables_from_pdf(uploaded_file)
    
    if tables:
        st.success(f"Found {len(tables)} tables")
        
        # Combine all tables
        combined_df = pd.concat(tables, ignore_index=True)
        
        st.dataframe(combined_df)
        
        # Convert to Excel in memory
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            combined_df.to_excel(writer, index=False, sheet_name="Extracted Data")
        
        output.seek(0)
        
        st.download_button(
            label="Download Excel File",
            data=output,
            file_name="converted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    else:
        st.error("No tables found in PDF")
