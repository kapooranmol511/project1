from fastapi import FastAPI, File, UploadFile, Query
import spacy
from fastapi.responses import JSONResponse
from pdf2image import convert_from_path
import pytesseract
import os
import shutil

nlp = spacy.load("en_core_web_sm")
app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the upload directory exists

def redact_sensitive_info(text):
    doc = nlp(text)
    redacted_text = text
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "EMAIL", "PHONE"]:
            redacted_text = redacted_text.replace(ent.text, "█████")
    return redacted_text

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...), redact: bool = Query(False)):
    # poppler_path = os.getenv("POPLER_PATH", "/opt/homebrew/bin")  # running on venv. 
    poppler_path = os.getenv("POPLER_PATH", "/usr/bin/")     # docker
    
    try:
        # Save the uploaded file to a temporary location
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        # Convert PDF to images using the saved file
        images = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)
        if not images:
            raise ValueError("No images were generated from the PDF.")

        # Perform OCR on each page
        ocr_results = []
        for page_number, image in enumerate(images):
            text = pytesseract.image_to_string(image)
            if redact:
                text = redact_sensitive_info(text)
            ocr_results.append({"page": page_number + 1, "text": text})

        return JSONResponse(content={"ocr_results": ocr_results})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        # Optional: Clean up the file after processing (comment this out if you want to keep the file)
        if os.path.exists(file_path):
            os.remove(file_path)


