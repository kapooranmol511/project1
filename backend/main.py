from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Read the PDF file
    pdf_reader = PdfReader(file.file)
    ocr_results = []

    # Process each page
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        # Convert PDF page to image
        image = page.to_image()
        # Perform OCR
        text = pytesseract.image_to_string(image)
        ocr_results.append({"page": page_number + 1, "text": text})

    return JSONResponse(content={"ocr_results": ocr_results})
