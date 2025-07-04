import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.docstore.document import Document

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def search_keywords_in_pdf(text, keyword):
    """
    Search for a keyword in the document using vector similarity,
    then summarize each of the top 5 chunks using GPT-4o.

    Returns a list of LangChain Document objects with GPT summaries.
    """
    # Split the text into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])

    # Create vector index
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Get top 5 semantically relevant chunks
    top_docs = retriever.get_relevant_documents(keyword)

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=openai_api_key)

    answers = []
    for i, doc in enumerate(top_docs):
        prompt = f"""
You are analyzing a company's annual report.

The keyword is: **{keyword}**

Read the following excerpt and extract all useful insights related to the keyword. Structure your response using short paragraphs or bullet points.

Excerpt:
\"\"\"
{doc.page_content}
\"\"\"
        """

        response = llm.predict(prompt.strip())
        answers.append(Document(page_content=response.strip()))

    return answers

