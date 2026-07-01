import re

def detect_pii(text):
    entities = []

    # ---------------- EMAIL ----------------
    for match in re.finditer(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    ):
        entities.append({
            "type": "EMAIL",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    # ---------------- PHONE ----------------
    for match in re.finditer(
        r"\b[6-9]\d{9}\b",
        text,
    ):
        entities.append({
            "type": "PHONE",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })

    # ---------------- AADHAAR ----------------
    aadhaar_pattern = r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"

    for match in re.finditer(aadhaar_pattern, text):
        entities.append({
            "type": "AADHAAR",
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })
        # PAN
    for match in re.finditer(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text):
     entities.append({
        "type":"PAN",
        "text":match.group(),
        "start":match.start(),
        "end":match.end()
    })

    return entities