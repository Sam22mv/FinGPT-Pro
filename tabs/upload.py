# tabs/upload.py

import streamlit as st
import re

# Global mappings
if "tickers" not in st.session_state:
    st.session_state["tickers"] = []

if "pdf_ticker_mapping" not in st.session_state:
    st.session_state["pdf_ticker_mapping"] = {}

# Extract ticker from filename
def extract_ticker_from_filename(filename):
    filename = filename.split('.')[0]
    parts = re.split(r'[-_]', filename)
    for part in parts:
        if part.isalpha() and len(part) >= 3:
            return part.upper()
    return None

def upload_tab():
    st.subheader("📂 Upload Annual Reports (PDFs)")
    pdf_files = st.file_uploader(
        "Upload PDF files (with tickers in filename)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

    if pdf_files:
        st.markdown("### 🔗 Auto-Mapped Tickers from Filenames")
        for pdf in pdf_files:
            ticker = extract_ticker_from_filename(pdf.name)
            if ticker:
                ticker = ticker.upper()
                if ticker not in st.session_state["tickers"]:
                    st.session_state["tickers"].append(ticker)
                    st.session_state["pdf_ticker_mapping"][ticker] = pdf
                    st.success(f"Mapped {pdf.name} → **{ticker}**")
            else:
                st.warning(f"Could not extract ticker from {pdf.name}")
