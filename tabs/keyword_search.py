# tabs/keyword_search.py

import streamlit as st
from utils.pdf_helper import extract_text_from_pdfs
from utils.rag_helper import search_keywords_in_pdf

def keyword_search_tab():
    st.header("🔍 Keyword Search in Annual Reports")

    tickers = st.session_state.get("tickers", [])
    pdf_mapping = st.session_state.get("pdf_ticker_mapping", {})

    if not tickers:
        st.info("Upload PDFs to use keyword search.")
        return

    keyword = st.text_input("Enter a keyword or phrase to search:")
    if st.button("Search"):
        for ticker in tickers:
            pdf = pdf_mapping.get(ticker)
            try:
                text = extract_text_from_pdfs([pdf])
                matches = search_keywords_in_pdf(text, keyword)
                result_str = "\n\n".join([doc.page_content.strip() for doc in matches])
                st.session_state[f"keyword_result_{ticker}"] = result_str
                st.markdown(f"### 🏢 {ticker}")
                st.markdown(result_str or "No matches found.")
            except Exception as e:
                st.error(f"❌ Error searching in {ticker}: {e}")
