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

    if st.button("Search") and keyword.strip():
        for ticker in tickers:
            pdf = pdf_mapping.get(ticker)
            if not pdf:
                st.warning(f"No PDF uploaded for {ticker}.")
                continue

            try:
                text = extract_text_from_pdfs([pdf])
                matches = search_keywords_in_pdf(text, keyword)

                st.markdown(f"### 🏢 {ticker}")

                if not matches:
                    st.markdown("❌ No matches found.")
                else:
                    st.markdown("#### 🧠 GPT-4o Answer:")
                    st.markdown(matches[0].page_content.strip())

                    # Save result for export tab
                    st.session_state[f"keyword_result_{ticker}"] = matches[0].page_content.strip()

            except Exception as e:
                st.error(f"❌ Error searching in {ticker}: {e}")
