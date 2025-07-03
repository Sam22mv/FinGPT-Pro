# tabs/news_sentiment.py

import streamlit as st
import requests
import plotly.express as px
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_news_headlines(query):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}&pageSize=3&sortBy=publishedAt"
        res = requests.get(url)
        data = res.json()
        if data.get("status") != "ok":
            return []
        return [article["title"] for article in data.get("articles", []) if "title" in article]
    except:
        return []

def analyze_sentiment_with_gpt(headline):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial sentiment analyst. Rate headlines as Positive, Negative, or Neutral."},
                {"role": "user", "content": f"Sentiment of this news: '{headline}'? One word only."}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except:
        return "Unknown"

def news_sentiment_tab():
    st.header("📰 News Sentiment Analysis")
    tickers = st.session_state.get("tickers", [])

    if not tickers:
        st.info("Upload PDFs to analyze news sentiment.")
        return

    for ticker in tickers:
        st.markdown(f"### 🏢 {ticker}")
        headlines = fetch_news_headlines(ticker)
        sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0, "Unknown": 0}

        for headline in headlines:
            sentiment = analyze_sentiment_with_gpt(headline)
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            st.write(f"**{headline}** — {sentiment}")

        fig = px.pie(
            names=list(sentiment_counts.keys()),
            values=list(sentiment_counts.values()),
            title="Sentiment Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
