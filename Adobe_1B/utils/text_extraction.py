import os
import fitz


def extract_text_from_pdfs(input_dir):
    pdf_data = {}
    if not os.path.exists(input_dir):
        return pdf_data
    for file in os.listdir(input_dir):
        if file.lower().endswith(".pdf"):
            path = os.path.join(input_dir, file)
            try:
                doc = fitz.open(path)
                pages = [page.get_text("text") for page in doc]
                pdf_data[file] = pages
                doc.close()
            except Exception:
                pdf_data[file] = [""]
    return pdf_data
