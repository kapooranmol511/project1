import streamlit as st
import requests

st.title("PDF OCR Application")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Send the file to the FastAPI backend
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://localhost:8000/upload-pdf/", files=files)

    if response.status_code == 200:
        ocr_results = response.json().get("ocr_results", [])
        for result in ocr_results:
            st.write(f"Page {result['page']}:")
            st.text(result['text'])
    else:
        st.error("Failed to process the PDF file.")
