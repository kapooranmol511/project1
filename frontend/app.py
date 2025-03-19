
import streamlit as st
import requests
from pdf2image import convert_from_bytes

st.title("PDF OCR Application")

redact_toggle = st.sidebar.checkbox("Redact sensitive information")
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Convert PDF to images
    try:
        images = convert_from_bytes(uploaded_file.getvalue())
        if not images:
            st.error("No images were generated from the PDF.")
    except Exception as e:
        st.error(f"Error converting PDF to images: {e}")
        images = []

    # Send the file to the FastAPI backend
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://localhost:8000/upload-pdf/", files=files, params={"redact": redact_toggle})

    if response.status_code == 200:
        ocr_results = response.json().get("ocr_results", [])

        # Create a two-column layout
        col1, col2 = st.columns(2)

        # Display images on the left
        with col1:
            page_number = st.number_input("Page", min_value=1, max_value=len(images), step=1)
            st.image(images[page_number - 1], use_column_width=True)

        # Display text on the right
        with col2:
            st.write(f"Page {page_number}:")
            st.text(ocr_results[page_number - 1]['text'] if page_number - 1 < len(ocr_results) else "No text available")
    else:
        st.error("Failed to process the PDF file.")

