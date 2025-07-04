# 💼 FinGPT Pro – AI-Powered Financial Report Analyzer 📊🧠

FinGPT Pro is an AI-powered Streamlit application that transforms **complex annual reports** into **actionable financial intelligence** using **GPT-4o** and **RAG (Retrieval-Augmented Generation)**.

Whether you're a financial analyst, investor, or researcher, FinGPT Pro helps you extract deep insights from corporate financials in seconds.

---

## 🚀 Live Demo

🔗 **[Try the App on Streamlit →](https://fingpt-pro-fpjj53nvp44pemdbygfn7a.streamlit.app/)**  
📂 Upload Annual Reports → 💬 Ask Questions → 📄 Export Custom Reports

---

## 🎥 Video Demo

📹 *Coming soon – walkthrough video demo with features*

---

## ✅ Features

| Feature                         | Description |
|---------------------------------|-------------|
| 🔍 **Keyword Search (GPT + RAG)** | Search any financial term (e.g. `profit`, `dividend`, `AI`) and get 5 GPT-4o structured answers from the PDF |
| 🧠 **Q&A Summary**               | GPT-4o summarizes the entire annual report into key insights |
| 📊 **SWOT Analysis**             | Auto-generated Strengths, Weaknesses, Opportunities, and Threats |
| 📰 **News Sentiment**            | Fetches and analyzes live news headlines related to the company |
| 📈 **Financial Charts**          | Visual trends for Revenue, Net Profit, and EPS using Plotly |
| 📄 **PDF Export**                | Download a polished report with all sections and graphs included |

---

## 🧠 Tech Stack

- **LLM Engine**: OpenAI `gpt-4o`
- **Framework**: Streamlit
- **RAG Pipeline**: LangChain + FAISS
- **PDF Parsing**: PyMuPDF (fitz)
- **Embedding Model**: OpenAI Embeddings
- **Vector DB**: FAISS
- **PDF Generation**: ReportLab
- **Charts**: Plotly
- **News + Data**: yFinance, Google News, GPT sentiment tagging

---

## 📂 Project Structure

## 🧠💡 What Makes FinGPT Pro Different?

Most LLM projects are either chatbots or basic PDF summarizers.

FinGPT Pro stands apart:

### 1. ✅ Document-grounded RAG  
No hallucinations. Every answer comes **only from your uploaded PDF**, not the internet.

### 2. ✅ Interactive & Structured  
Supports **semantic keyword search** across the document, not just basic keyword matching.

### 3. ✅ GPT-4o + LangChain Stack  
Uses a full **RAG pipeline**: FAISS for top-k retrieval + GPT-4o for clean summaries.

### 4. ✅ Built for Finance  
Includes **domain-specific features** like SWOT, charts, news sentiment, and mock financials.

### 5. ✅ Full Exportable Report  
Unlike most apps, you can **download a clean report** with summaries, GPT answers, and visuals.

---
## ⚙️ Getting Started (Local Setup)

Follow these steps to run the project locally:

# 1. Clone the repository
git clone https://github.com/Sam22mv/FinGPT-Pro.git
cd FinGPT-Pro

# 2. Create a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenAI API key
echo OPENAI_API_KEY=your-key-here > .env

# 5. Run the Streamlit app
streamlit run app.py

```bash

```bash
FinGPT-Pro/
│
├── app.py                         # Main Streamlit app
├── tabs/
│   ├── summary.py                 # GPT Q&A summarization
│   ├── swot.py                    # GPT-based SWOT
│   ├── keyword_search.py          # Keyword search (RAG)
│   └── export.py                  # PDF generation
│
├── utils/
│   ├── rag_helper.py              # Vector DB + GPT querying
│   ├── pdf_helper.py              # Extract raw text from PDFs
│   ├── portfolio_helper.py        # Financial data retrieval
│
├── data/                          # Uploaded PDFs
├── requirements.txt               # Python dependencies
├── .env                           # OpenAI API key (do not share)
└── README.md
---
