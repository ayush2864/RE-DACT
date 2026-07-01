import fitz

def redact_pdf(input_pdf, output_pdf, entities, ocr_data=None):

    doc = fitz.open(input_pdf)

    for page_number, page in enumerate(doc):

        print("Page Size:", page.rect)

        # Digital PDF
        if ocr_data is None or len(ocr_data) == 0:

            for entity in entities:

                areas = page.search_for(entity["text"])

                for area in areas:
                    page.add_redact_annot(area, fill=(0, 0, 0))

            page.apply_redactions()

        # Scanned PDF
        else:

            if page_number >= len(ocr_data):
                continue

            # Image size used by OCR
            pix = page.get_pixmap(dpi=300)

            scale_x = page.rect.width / pix.width
            scale_y = page.rect.height / pix.height

            for box, text, confidence in ocr_data[page_number]:

                ocr_text = text.replace(" ", "")

                for entity in entities:

                    entity_text = entity["text"].replace(" ", "")

                    if entity_text in ocr_text:

                        x1 = float(box[0][0]) * scale_x
                        y1 = float(box[0][1]) * scale_y
                        x2 = float(box[2][0]) * scale_x
                        y2 = float(box[2][1]) * scale_y

                        rect = fitz.Rect(x1, y1, x2, y2)

                        print("Redacting:", entity["text"])
                        print(rect)

                        page.add_redact_annot(
                            rect,
                            fill=(0, 0, 0)
                        )

            page.apply_redactions()

    doc.save(output_pdf)
    doc.close()