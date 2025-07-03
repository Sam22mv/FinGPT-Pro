# utils/pdf_helper.py

import fitz  # PyMuPDF
import re

def extract_text_from_pdfs(pdf_files):
    """
    Extracts and concatenates text from a list of PDF file-like objects.
    """
    all_text = ""
    for pdf in pdf_files:
        pdf.seek(0)  # Reset file pointer
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for page in doc:
                all_text += page.get_text()
    return all_text

def extract_financials_from_pdf(text):
    """
    Extracts key financial metrics like Revenue, Net Profit, and EPS from PDF text using regex patterns.
    """
    metrics = {}

    patterns = {
        "Revenue": r"Revenues\*?\s+([\d,]+(?:\.\d+)?)",
        "Net Profit": r"Net\s+profit\*?#?\s+([\d,]+(?:\.\d+)?)",
        "EPS": r"Basic\s+earnings\s+per\s+share\s+\(.*?₹.*?\)\*?\s*([\d,]+(?:\.\d+)?)"
    }

    for label, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics[label] = match.group(1)
        else:
            metrics[label] = "Not Found"

    return metrics
