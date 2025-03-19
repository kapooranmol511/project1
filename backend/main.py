from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
import pytesseract
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload directory exists

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    poppler_path = "/opt/homebrew/bin"  # Update based on your Poppler installation

    try:
        # Save the uploaded file to a temporary location
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        # Convert PDF to images using the saved file
        images = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)

        # Perform OCR on each page
        ocr_results = []
        for page_number, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            ocr_results.append({"page": page_number + 1, "text": text})

        return JSONResponse(content={"ocr_results": ocr_results})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Optional: Clean up the file after processing (comment this out if you want to keep the file)
        if os.path.exists(file_path):
            os.remove(file_path)


