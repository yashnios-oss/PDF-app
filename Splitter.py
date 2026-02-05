import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Page Splitter", page_icon="✂️")

st.title("✂️ PDF Page Splitter")
st.write("Upload a PDF and select the pages you want to extract into a new file.")

# File Uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    # Fix: Use len(reader.pages) instead of len(reader)
    total_pages = len(reader.pages) 
    
    st.info(f"This PDF has **{total_pages}** pages.")

    page_selection = st.text_input(
        "Enter pages or ranges (e.g., 1, 2, 5-10):",
        placeholder="1-3, 5"
    )

    if page_selection:
        try:
            selected_pages = []
            parts = page_selection.split(',')
            
            for part in parts:
                part = part.strip() # Handle accidental spaces
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    selected_pages.extend(range(start, end + 1))
                else:
                    selected_pages.append(int(part))

            selected_pages = sorted(list(set(selected_pages)))
            
            if max(selected_pages) > total_pages or min(selected_pages) < 1:
                st.error(f"Please enter page numbers between 1 and {total_pages}.")
            else:
                writer = PdfWriter()
                for p in selected_pages:
                    # Accessing pages via reader.pages[index]
                    writer.add_page(reader.pages[p - 1])

                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)

                st.success(f"Successfully prepared {len(selected_pages)} pages!")
                st.download_button(
                    label="Download Split PDF",
                    data=output_pdf,
                    file_name="split_document.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Invalid input format. Error: {e}")


    if page_selection:
        try:
            # Logic to parse the page selection
            selected_pages = []
            parts = page_selection.split(',')
            
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    selected_pages.extend(range(start, end + 1))
                else:
                    selected_pages.append(int(part))

            # Remove duplicates and adjust for 0-based indexing
            selected_pages = sorted(list(set(selected_pages)))
            
            # Validation
            if max(selected_pages) > total_pages or min(selected_pages) < 1:
                st.error(f"Please enter page numbers between 1 and {total_pages}.")
            else:
                # PDF Processing
                writer = PdfWriter()
                for p in selected_pages:
                    writer.add_page(reader.pages[p - 1])

                # Prepare for download
                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)

                st.success(f"Successfully prepared {len(selected_pages)} pages!")
                
                st.download_button(
                    label="Download Split PDF",
                    data=output_pdf,
                    file_name="split_document.pdf",
                    mime="application/pdf"
                )

        except ValueError:
            st.warning("Please use the correct format (e.g., 1-5 or 1, 2, 3).")

