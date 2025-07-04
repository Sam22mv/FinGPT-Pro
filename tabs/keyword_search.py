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
                st.warning(f"⚠️ No PDF uploaded for {ticker}.")
                continue

            try:
                st.markdown(f"### 🏢 {ticker}")
                st.markdown("⏳ Searching...")

                text = extract_text_from_pdfs([pdf])
                matches = search_keywords_in_pdf(text, keyword)

                if not matches:
                    st.markdown("❌ No relevant information found.")
                else:
                    combined_output = []
                    for i, doc in enumerate(matches):
                        st.markdown(f"**🔹 GPT Answer {i+1}:**")
                        st.write(doc.page_content)
                        combined_output.append(doc.page_content)
                        st.markdown("---")

                    st.session_state[f"keyword_result_{ticker}"] = "\n\n".join(combined_output)

            except Exception as e:
                st.error(f"❌ Error processing {ticker}: {e}")


