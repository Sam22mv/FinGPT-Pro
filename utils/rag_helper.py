# utils/rag_helper.py

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def build_rag_chain_from_text(text):
    """
    Build a LangChain Retrieval-Augmented Generation (RAG) pipeline
    for answering questions based on PDF text.

    Returns a RetrievalQA chain object.
    """
    # Step 1: Split text into chunks for embedding
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    # Step 2: Create embeddings and FAISS vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    # Step 3: Initialize GPT-4o based retriever QA chain
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=openai_api_key)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(),
        return_source_documents=False
    )
    return qa_chain


def search_keywords_in_pdf(text, keyword):
    """
    Perform semantic keyword search on PDF text and return
    the top 5 most relevant document chunks.

    Returns a list of Document objects.
    """
    # Step 1: Split text into documents with overlap for context
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])

    # Step 2: Create embeddings and FAISS vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Step 3: Perform semantic similarity search
    results = vectorstore.similarity_search(keyword, k=5)
    return results
