




import fitz
import pytesseract
from pdf2image import convert_from_path

# ✅ YOUR POPPLER PATH
POPPLER_PATH = r"C:\Users\DELL\Downloads\poppler-25.12.0\Library\bin"


def extract_pdf_text(pdf_path):
    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        # ✅ OCR fallback if text is low
        if len(text.strip()) < 100:
            print(f"🔍 OCR used for: {pdf_path}")

            images = convert_from_path(
                pdf_path,
                poppler_path=POPPLER_PATH
            )

            for img in images:
                text += pytesseract.image_to_string(img)

    except Exception as e:
        print("PDF parsing error:", e)

    return text



# import fitz  # PyMuPDF
# import pytesseract
# from pdf2image import convert_from_path


# def extract_pdf_text(pdf_path):
#     text = ""

#     try:
#         # ✅ Try normal text extraction
#         doc = fitz.open(pdf_path)

#         for page in doc:
#             text += page.get_text()

#         # 🔥 If text too small → use OCR
#         if len(text.strip()) < 100:
#             print(f"OCR used for: {pdf_path}")

#             images = convert_from_path(pdf_path)

#             for img in images:
#                 text += pytesseract.image_to_string(img)

#     except Exception as e:
#         print("PDF parsing error:", e)

#     return text






















# import pdfplumber

# def extract_pdf_text(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""
#     return text