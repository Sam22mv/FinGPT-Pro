# tabs/swot.py

import streamlit as st
from utils.portfolio_helper import get_mock_financial_metrics, get_financial_metrics_yfinance
from utils.pdf_helper import extract_text_from_pdfs
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def swot_tab():
    st.header("💡 GPT SWOT Analysis")

    tickers = st.session_state.get("tickers", [])
    pdf_mapping = st.session_state.get("pdf_ticker_mapping", {})
    market = st.session_state.get("market", "🇮🇳 Indian")

    if not tickers:
        st.info("Upload PDFs to view SWOT analysis.")
        return

    for ticker in tickers:
        try:
            pdf_text = extract_text_from_pdfs([pdf_mapping[ticker]])[:2000]
            web_metrics = (
                get_mock_financial_metrics(ticker)
                if market == "🇮🇳 Indian"
                else get_financial_metrics_yfinance(ticker)
            )
            web_context = "\n".join([f"{k}: ₹{v}" for k, v in web_metrics.items()])
            manual_context = "\n".join([f"{k}: {v}" for k, v in st.session_state.get(f"manual_data_{ticker}", {}).items()])

            prompt = f"""
You are a financial analyst. Based on the below:
### Web ###\n{web_context}
### Manual ###\n{manual_context}
### PDF ###\n{pdf_text}
Give SWOT analysis with bullet points.
"""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": prompt}
                ]
            )
            swot_result = response.choices[0].message.content.strip()
            st.session_state[f"swot_{ticker}"] = swot_result
            st.markdown(f"### 🏢 {ticker}")
            st.markdown(swot_result)
        except Exception as e:
            st.error(f"❌ SWOT analysis error for {ticker}: {e}")
