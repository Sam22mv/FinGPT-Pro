import streamlit as st

# set_page_config MUST be first Streamlit command
st.set_page_config(page_title="FinGPT Pro", layout="wide", page_icon="🏢")

import sys
import os
from dotenv import load_dotenv

# optional: check Python executable (for debugging)
st.write("Python executable:", sys.executable)

# ---- Page Styling ----
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- Load Environment Variables ----
load_dotenv()

# ---- Initialize session state keys ----
if "tickers" not in st.session_state:
    st.session_state["tickers"] = []

if "pdf_ticker_mapping" not in st.session_state:
    st.session_state["pdf_ticker_mapping"] = {}

if "market" not in st.session_state:
    st.session_state["market"] = "🇮🇳 Indian"  # default market

# ---- Market Selector in Sidebar ----
st.session_state["market"] = st.sidebar.radio(
    "Choose market type:", ("🇮🇳 Indian", "🌍 Foreign"),
    index=0 if st.session_state["market"] == "🇮🇳 Indian" else 1
)

# ---- App Title ----
st.markdown("<h1 style='text-align: center; color: white;'>📊 FinGPT Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: gray;'>AI-Powered Portfolio Intelligence & Report Automation</p>", unsafe_allow_html=True)

# ---- Tab Imports ----
from tabs.upload import upload_tab
from tabs.dashboard import dashboard_tab
from tabs.news_sentiment import news_sentiment_tab
from tabs.keyword_search import keyword_search_tab
from tabs.gpt_qa import gpt_qa_tab
from tabs.swot import swot_tab
from tabs.export import export_tab

# ---- Create Tabs ----
tabs = st.tabs([
    "📂 Upload PDFs & Tickers",
    "📈 Dashboard",
    "📰 News Sentiment",
    "🔍 Keyword Search",
    "🧠 GPT Q&A",
    "💡 GPT SWOT Analysis",
    "📄 PDF Export"
])

with tabs[0]:
    upload_tab()

with tabs[1]:
    dashboard_tab()

with tabs[2]:
    news_sentiment_tab()

with tabs[3]:
    keyword_search_tab()

with tabs[4]:
    gpt_qa_tab()

with tabs[5]:
    swot_tab()

with tabs[6]:
    export_tab()

# ---- Footer ----
st.markdown("---")
st.markdown("© 2025 MV Sam | FinGPT Pro: AI-Powered Portfolio Insights with GPT-4o")


