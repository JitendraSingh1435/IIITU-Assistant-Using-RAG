import json
import os
import pickle

from langchain.docstore.document import Document
from tqdm import tqdm

from embeddings.embedding_model import get_embedding_model
from processing.pdf_downloader import download_pdfs
from processing.pdf_parser import extract_pdf_text
from processing.table_extractor import extract_tables
from processing.text_cleaner import clean_text
from rag.rag_pipeline import generate_answer
from retriever.retriever import CustomRetriever
from vectorstore.faiss_store import create_faiss, load_faiss


FAISS_PATH = "faiss_index"
DOC_CACHE = "data/processed/docs.pkl"
RAW_DATA_PATH = "data/raw/output.json"
PDF_FOLDER = "data/pdfs"
PROCESSED_DIR = "data/processed"
WEB_LOG = os.path.join(PROCESSED_DIR, "web_done.txt")
PDF_LOG = os.path.join(PROCESSED_DIR, "pdfs_done.txt")


def ensure_processed_dir():
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_raw_data(path=RAW_DATA_PATH):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def read_processed_items(log_path):
    if not os.path.exists(log_path):
        return set()

    with open(log_path, "r", encoding="utf-8") as file:
        return set(file.read().splitlines())


def append_processed_item(log_path, value):
    with open(log_path, "a", encoding="utf-8") as file:
        file.write(f"{value}\n")


def build_documents(data):
    ensure_processed_dir()
    docs = []
    done_urls = read_processed_items(WEB_LOG)

    for item in tqdm(data, desc="Processing website data"):
        url = item.get("url", "")
        if url in done_urls:
            continue

        text = clean_text(item.get("text", ""))
        tables = extract_tables(item.get("tables", []))

        content_parts = [part for part in [text, "\n".join(tables)] if part.strip()]
        if not content_parts:
            continue

        docs.append(
            Document(
                page_content="\n\n".join(content_parts),
                metadata={"source": url, "type": "web"},
            )
        )
        append_processed_item(WEB_LOG, url)

    return docs


def load_pdf_documents(folder_path=PDF_FOLDER):
    ensure_processed_dir()
    docs = []
    done_files = read_processed_items(PDF_LOG)

    if not os.path.exists(folder_path):
        return docs

    files = [file for file in os.listdir(folder_path) if file.lower().endswith(".pdf")]

    for file in tqdm(files, desc="Processing PDFs"):
        if file in done_files:
            continue

        path = os.path.join(folder_path, file)
        text = extract_pdf_text(path)

        if not text.strip():
            continue

        docs.append(
            Document(
                page_content=text,
                metadata={"source": file, "type": "pdf"},
            )
        )
        append_processed_item(PDF_LOG, file)

    return docs


def load_cached_documents():
    if not os.path.exists(DOC_CACHE):
        return None

    with open(DOC_CACHE, "rb") as file:
        return pickle.load(file)


def save_cached_documents(docs):
    ensure_processed_dir()
    with open(DOC_CACHE, "wb") as file:
        pickle.dump(docs, file)


def build_corpus():
    data = load_raw_data()
    download_pdfs(data)

    cached_docs = load_cached_documents()
    if cached_docs is not None:
        return cached_docs

    web_docs = build_documents(data)
    pdf_docs = load_pdf_documents(PDF_FOLDER)
    docs = web_docs + pdf_docs

    if not docs:
        raise ValueError("No documents found to build the vector store.")

    save_cached_documents(docs)
    return docs


def get_vectorstore():
    embedding_model = get_embedding_model()

    if os.path.exists(FAISS_PATH):
        print("Loading existing FAISS index...")
        return load_faiss(embedding_model)

    print("Creating FAISS index...")
    docs = build_corpus()
    return create_faiss(docs, embedding_model)


def get_retriever(k=8):
    vectorstore = get_vectorstore()
    return CustomRetriever(vectorstore, k=k)


def answer_query(query, k=8):
    retriever = get_retriever(k=k)
    docs = retriever.get_docs(query)
    answer = generate_answer(query, docs, verbose=False)
    return answer, docs


def run_cli():
    retriever = get_retriever()

    print("\nSystem ready. Ask your questions.\n")

    while True:
        query = input("Ask (type 'exit' to quit): ").strip()

        if query.lower() == "exit":
            break

        if not query:
            print("Please enter a question.")
            continue

        docs = retriever.get_docs(query)
        answer = generate_answer(query, docs)
        print("\nAnswer:\n", answer)


if __name__ == "__main__":
    run_cli()
