# utils/gpt_helper.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client once to reuse
client = OpenAI(api_key=api_key)

def get_financial_summary(ticker: str, market: str) -> str:
    """
    Uses OpenAI GPT model to generate a financial summary for a given stock ticker and market.
    """
    prompt = f"""
You are a financial analyst. Summarize the financial performance and outlook for the stock ticker '{ticker}'.
The company belongs to the {market} market.
Include insights like revenue trend, net profit, and EPS if publicly known, else give a general summary based on public data.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Error] GPT summary failed: {e}"
