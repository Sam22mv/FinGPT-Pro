# 💼 FinGPT Pro – AI-Powered Financial Report Analyzer 📊🧠

FinGPT Pro is a powerful AI application that analyzes **annual reports** using **GPT-4o** and **RAG (Retrieval-Augmented Generation)** to deliver:

- 🔍 Keyword-specific semantic search
- 🧠 GPT-4o structured summaries
- 📊 SWOT analysis
- 📰 News sentiment analysis
- 📈 Financial trends visualization
- 📄 PDF export with a complete report

Built for financial analysts, researchers, and investors who need deep insights from complex financial documents.

---

## 🚀 Live Demo

🔗 **[Streamlit App](https://fingpt-pro.streamlit.app)**  
📂 Upload PDFs → 🧠 Ask Financial Questions → 📄 Export Reports

---

## 📌 Features

| Feature                     | Description |
|----------------------------|-------------|
| 🔍 **Keyword Search (GPT + RAG)** | Search any keyword like "profit", "AI", or "dividend" and get GPT-4o structured answers based on PDF content |
| 🧠 **Q&A Summary**           | GPT-generated summary of the full annual report |
| 📊 **SWOT Analysis**         | GPT-4o generates Strengths, Weaknesses, Opportunities, Threats |
| 📰 **News Sentiment**        | Fetches recent headlines and analyzes sentiment using GPT |
| 📈 **Financial Charts**      | Trendlines for Revenue, Profit, EPS using Plotly |
| 📄 **PDF Export**            | Full report downloadable in a clean PDF format |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4o
- **RAG Pipeline**: LangChain + FAISS
- **Embedding**: OpenAI Embeddings
- **Vector Store**: FAISS
- **PDF Generation**: ReportLab
- **Charting**: Plotly
- **News & Data**: yFinance, Google News

---

## 📂 Project Structure

```bash
FinGPT-Pro/
│
├── app.py                         # Main Streamlit app entry point
├── tabs/
│   ├── summary.py                 # GPT-based summary
│   ├── swot.py                    # SWOT analysis via GPT
│   ├── keyword_search.py          # Keyword search via RAG
│   └── export.py                  # Generate and download PDF
│
├── utils/
│   ├── rag_helper.py              # RAG logic and GPT integration
│   ├── pdf_helper.py              # Extract text from PDF files
│   ├── portfolio_helper.py        # Get financial metrics
│
├── data/                          # Uploaded PDFs
├── requirements.txt
├── .env                           # Your API key
└── README.md
