from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import time
import fitz

from app.services.ocr_service import extract_text
from app.services.pii_service import detect_pii
from app.services.redaction_service import redact_pdf

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "uploads")
)

OUTPUT_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "outputs")
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@router.get("/")
def home():
    return {
        "message": "RE-DACT API Running"
    }


@router.get("/test-pii")
def test_pii():

    text = "My phone is 9876543210 and Aadhaar is 1234 5678 9012"

    entities = detect_pii(text)

    return {
        "text": text,
        "entities": entities
    }


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    start_time = time.time()

    input_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = round(
        os.path.getsize(input_path) / 1024,
        2
    )

    doc = fitz.open(input_path)
    pages = len(doc)
    doc.close()

    result = extract_text(input_path)

    text = result["text"]
    ocr_data = result["ocr_data"]

    entities = detect_pii(text)

    output_filename = "redacted_" + file.filename

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    redact_pdf(
        input_pdf=input_path,
        output_pdf=output_path,
        ocr_data=ocr_data,
        entities=entities
    )

    processing_time = round(
        time.time() - start_time,
        2
    )

    return {

        "filename": output_filename,

        "text": text,

        "entities": entities,

        "pages": pages,

        "pii_count": len(entities),

        "processing_time": processing_time,

        "file_size": f"{file_size} KB"

    }


@router.get("/download/{filename}")
def download_file(filename: str):

    path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=filename
    )