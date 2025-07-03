# tabs/gpt_qa.py

import streamlit as st
from utils.portfolio_helper import get_mock_financial_metrics, get_financial_metrics_yfinance
from utils.pdf_helper import extract_text_from_pdfs
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_qa_tab():
    st.header("🧠 GPT Q&A – Ask about Financials")

    tickers = st.session_state.get("tickers", [])
    pdf_mapping = st.session_state.get("pdf_ticker_mapping", {})
    market = st.session_state.get("market", "🇮🇳 Indian")

    if not tickers:
        st.info("Upload PDFs to ask financial questions.")
        return

    question = st.text_input("Enter your question about the company financials:")
    if st.button("Ask GPT"):
        for ticker in tickers:
            try:
                pdf_text = extract_text_from_pdfs([pdf_mapping[ticker]])[:2000]
                web_metrics = (
                    get_mock_financial_metrics(ticker)
                    if market == "🇮🇳 Indian"
                    else get_financial_metrics_yfinance(ticker)
                )
                web_context = "\n".join([f"{k}: ₹{v}" for k, v in web_metrics.items()])
                prompt = f"""
You are a financial analyst.
### Web Metrics ###\n{web_context}
### PDF Extract ###\n{pdf_text}
### Question ###\n{question}
Answer using insights from both web and PDF.
"""
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a financial analyst."},
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content.strip()
                st.session_state[f"qa_{ticker}"] = answer
                st.markdown(f"### 🏢 {ticker}")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ GPT error for {ticker}: {e}")
