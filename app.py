import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Pro PDF Converter")
st.title("🚀 Heavy-Duty PDF to Excel")
st.write("Optimized for large documents (up to 500+ pages)")

uploaded_file = st.file_uploader("Upload a large PDF", type="pdf")

if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            total_pages = len(pdf.pages)
            all_tables = []
            
            # Create a progress bar for the user
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, page in enumerate(pdf.pages):
                # Update progress
                progress = (i + 1) / total_pages
                progress_bar.progress(progress)
                status_text.text(f"Processing page {i+1} of {total_pages}...")
                
                # Extract table
                table = page.extract_table()
                if table:
                    # Clean the table slightly to save memory
                    df = pd.DataFrame(table)
                    all_tables.append(df)
                
                # Memory management: Stop if it gets too huge for the free tier
                if len(all_tables) > 1000: 
                    st.warning("Document is extremely large. Only the first 1000 tables were captured.")
                    break

            if all_tables:
                status_text.text("Finalizing Excel file... please wait.")
                final_df = pd.concat(all_tables, ignore_index=True)
                
                # Convert to Excel
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False)
                
                st.success("✅ Done!")
                st.download_button(
                    label="📥 Download Huge Excel File",
                    data=output.getvalue(),
                    file_name="large_data_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("No tables were found in those 500 pages.")
                
    except Exception as e:
        st.error(f"The app hit a limit: {e}")
