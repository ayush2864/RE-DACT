import fitz
import easyocr
import numpy as np
from PIL import Image
from docx import Document
import os

reader = easyocr.Reader(['en'], gpu=False)


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    # IMAGE
    if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        result = reader.readtext(file_path, detail=1)

        text = " ".join([r[1] for r in result])

        return {
            "text": text,
            "ocr_data": result
        }

    # PDF
    elif ext == ".pdf":

        print("PDF detected")

        doc = fitz.open(file_path)

        extracted_text = ""
        ocr_data = []

        for i, page in enumerate(doc):

            text = page.get_text("text").strip()

            print(f"Page {i+1}")
            print("Text length:", len(text))

            if text:

                print("Digital PDF")

                extracted_text += text + "\n"

            else:

                print("Scanned PDF -> Running OCR")

                pix = page.get_pixmap(dpi=300)

                img = Image.frombytes(
                    "RGB",
                    (pix.width, pix.height),
                    pix.samples
                )

                result = reader.readtext(
                    np.array(img),
                    detail=1
                )

                print("OCR Result:", result)

                ocr_data.append(result)

                extracted_text += " ".join(
                    [r[1] for r in result]
                ) + "\n"

        doc.close()

        return {
            "text": extracted_text,
            "ocr_data": ocr_data
        }

    # DOCX
    elif ext == ".docx":

        doc = Document(file_path)

        return {
            "text": "\n".join([p.text for p in doc.paragraphs]),
            "ocr_data": None
        }

    else:
        raise Exception(f"Unsupported file type: {ext}")