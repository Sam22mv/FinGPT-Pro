import streamlit as st
from utils.pdf_helper import extract_text_from_pdfs
from utils.rag_helper import build_rag_chain_from_text

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

                # Extract and embed the full PDF text
                text = extract_text_from_pdfs([pdf])
                qa_chain = build_rag_chain_from_text(text)

                # Ask GPT-4o to give structured answer
                prompt = (
                    f"Summarize all useful insights and mentions related to the keyword: '{keyword}' "
                    f"in this company's annual report. Use bullet points or paragraph structure where suitable."
                )
                gpt_answer = qa_chain.run(prompt.strip())

                st.markdown("#### 🧠 GPT-4o Answer:")
                if gpt_answer:
                    st.markdown(gpt_answer)
                    st.session_state[f"keyword_result_{ticker}"] = gpt_answer
                else:
                    st.markdown("❌ No relevant information found.")

            except Exception as e:
                st.error(f"❌ Error processing {ticker}: {e}")
