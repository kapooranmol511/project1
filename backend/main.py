from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    poppler_path = "/opt/homebrew/bin"  # Ensure this matches your Poppler installation path

    images = convert_from_bytes(file.file.read(), dpi=300, poppler_path=poppler_path)

    ocr_results = []
    for page_number, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        ocr_results.append({"page": page_number + 1, "text": text})

    return JSONResponse(content={"ocr_results": ocr_results})



# @app.post("/upload-pdf/")
# async def upload_pdf(file: UploadFile = File(...)):
#     # Read the PDF file
#     pdf_reader = PdfReader(file.file)
#     ocr_results = []

#     # Process each page
#     for page_number in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_number]
#         # Convert PDF page to image
#         image = page.to_image()
#         # Perform OCR
#         text = pytesseract.image_to_string(image)
#         ocr_results.append({"page": page_number + 1, "text": text})

#     return JSONResponse(content={"ocr_results": ocr_results})

