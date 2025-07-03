# tabs/dashboard.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.portfolio_helper import get_mock_financial_metrics, get_financial_metrics_yfinance, get_historical_data
from utils.pdf_helper import extract_text_from_pdfs
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def dashboard_tab():
    st.header("📊 Portfolio Dashboard")
    tickers = st.session_state.get("tickers", [])
    market = st.session_state.get("market", "🇮🇳 Indian")

    if not tickers:
        st.info("Upload PDFs to view dashboard.")
        return

    for ticker in tickers:
        st.subheader(f"🏢 {ticker} Overview")

        metrics = (
            get_mock_financial_metrics(ticker)
            if market == "🇮🇳 Indian"
            else get_financial_metrics_yfinance(ticker)
        )

        # Display metrics
        cols = st.columns(3)
        for idx, (label, value) in enumerate(metrics.items()):
            cols[idx].metric(label=label, value=value)

        # Sector pie chart (mocked)
        pie_fig = px.pie(names=["IT", "Finance", "Pharma", "Energy"], values=[30, 25, 20, 25])
        st.plotly_chart(pie_fig, use_container_width=True)

        # Trend line chart
        hist_data = get_historical_data(ticker)
        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(x=hist_data["Year"], y=hist_data["Revenue"], mode='lines+markers', name='Revenue'))
        trend_fig.add_trace(go.Scatter(x=hist_data["Year"], y=hist_data["Net Profit"], mode='lines+markers', name='Net Profit'))
        trend_fig.add_trace(go.Scatter(x=hist_data["Year"], y=hist_data["EPS"], mode='lines+markers', name='EPS'))
        st.plotly_chart(trend_fig, use_container_width=True)

        # GPT Summary
        try:
            pdf = st.session_state["pdf_ticker_mapping"][ticker]
            pdf_text = extract_text_from_pdfs([pdf])[:2000]
            web_context = "\n".join([f"{k}: ₹{v}" for k, v in metrics.items()])
            gpt_prompt = f"""
You are a financial analyst. Based on the below:
### Web Financials ###\n{web_context}
### PDF Extract ###\n{pdf_text}
Write a summary with key financial insights.
"""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a financial analyst."},
                    {"role": "user", "content": gpt_prompt}
                ]
            )
            summary = response.choices[0].message.content.strip()
            st.session_state[f"summary_{ticker}"] = summary
            st.markdown("#### 🧠 GPT Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"GPT Summary Error: {e}")
