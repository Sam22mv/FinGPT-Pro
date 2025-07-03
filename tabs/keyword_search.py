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
                    for i, doc in enumerate(matches):
                        snippet = doc.page_content.strip()
                        if len(snippet) > 500:
                            snippet = snippet[:500] + "..."
                        st.markdown(f"**Match {i+1}:**")
                        st.code(snippet)
                        st.markdown("---")

                # Save result to session state for export tab
                combined_results = "\n\n".join(doc.page_content.strip()[:500] + "..." if len(doc.page_content.strip()) > 500 else doc.page_content.strip() for doc in matches)
                st.session_state[f"keyword_result_{ticker}"] = combined_results or "No keyword matches found"

            except Exception as e:
                st.error(f"❌ Error searching in {ticker}: {e}")

