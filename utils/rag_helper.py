# utils/rag_helper.py

import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def build_rag_chain_from_text(text):
    """
    Build a LangChain Retrieval-Augmented Generation (RAG) pipeline
    for answering questions based on PDF text.

    Returns a RetrievalQA chain object.
    """
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)

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
    5 structured GPT-4o responses, one per matched chunk.

    Returns a list of Document objects.
    """
    # Step 1: Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])

    # Step 2: Embed and store chunks in FAISS
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Step 3: Use GPT-4o to answer for each top chunk
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=openai_api_key)

    # Get top 5 chunks semantically related to keyword
    top_docs = retriever.get_relevant_documents(keyword)
    answers = []

    for i, doc in enumerate(top_docs):
        prompt = f"""
        You are reading a company annual report.

        From the following report excerpt, generate a **clear, structured response** related to the keyword: **'{keyword}'**

        Keep your answer informative and concise using bullet points if appropriate.

        Document Chunk:
        \"\"\"
        {doc.page_content}
        \"\"\"
        """

        response = llm.predict(prompt.strip())
        answers.append(Document(page_content=response.strip()))

    return answers
