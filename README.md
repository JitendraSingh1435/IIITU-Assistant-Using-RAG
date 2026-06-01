#  🎓 IIITU Assistant using RAG

An AI-powered Retrieval-Augmented Generation (RAG) assistant built for the Indian Institute of Information Technology Una (IIIT Una).

The assistant scrapes content from the official IIIT Una website, processes web pages, PDFs, tables, and images, generates embeddings, stores them in a FAISS vector database, and answers user queries using Google's Gemini model.

---

## ✨ Features

- 🌐 Web scraping of IIIT Una website
- 📄 Automatic PDF discovery and downloading
- 📑 PDF text extraction and processing
- 📊 Table extraction and indexing
- 🖼️ Image content processing
- 🔍 Semantic search using FAISS
- 🤖 Retrieval-Augmented Generation (RAG)
- ⚡ Gemini-powered answer generation
- 💻 Streamlit-based chat interface

---

## 🏗️ Project Architecture

```text
User Query
    │
    ▼
Retriever (FAISS)
    │
    ▼
Relevant Documents
    │
    ▼
Gemini 2.5 Flash
    │
    ▼
Generated Answer
```

---

## 📂 Project Structure

```text
IIITU-RAG-Assistant/
│
├── app.py                     # Streamlit application
├── main.py                    # Pipeline orchestration
├── requirements.txt
├── .env                       # Environment variables (not included)
│
├── crawler/
│   ├── selenium_crawler.py
│   └── scrapy_project/
│
├── processing/
│   ├── pdf_downloader.py
│   ├── pdf_parser.py
│   ├── table_extractor.py
│   ├── image_processor.py
│   └── text_cleaner.py
│
├── embeddings/
│   └── embedding_model.py
│
├── vectorstore/
│   └── faiss_store.py
│
├── retriever/
│   └── retriever.py
│
├── rag/
│   └── rag_pipeline.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── pdfs/
│   └── images/
│
└── faiss_index/               # Generated after vector store creation
```

---

## 📁 Data Directory

The `data/` folder is not included in this repository.

It is automatically populated during the scraping and processing pipeline.

Expected structure:

```text
data/
│
├── raw/
│   └── output.json
│
├── pdfs/
│   └── Downloaded PDFs from IIIT Una website
│
├── images/
│   └── Downloaded website images
│
└── processed/
    ├── docs.pkl
    ├── embeddings.pkl
    ├── pdfs_done.txt
    └── web_done.txt
```

### 📌 Folder Description

| Folder | Purpose |
|----------|----------|
| 📄 raw | Stores scraped website content |
| 📚 pdfs | Stores downloaded PDFs from IIIT Una website |
| 🖼️ images | Stores downloaded website images |
| ⚙️ processed | Stores processed documents, embeddings, and logs |


---

## 🧠 FAISS Index
  
The `faiss_index/` folder is not included in the repository.

It is automatically generated when creating the vector database.

Generated structure:

```text
faiss_index/
│
├── index.faiss
└── index.pkl
```

These files contain the vector embeddings and metadata used for semantic retrieval.

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_api_key
```

The project uses:

- Gemini 2.5 Flash
- Google Generative AI SDK

---

## 🚀 Installation

### 📥 Clone Repository

```bash
git clone https://github.com/yourusername/iiitu-rag-assistant.git

cd iiitu-rag-assistant
```

### 🐍 Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Building the Knowledge Base

### 1️⃣ Crawl IIIT Una Website

Run the crawler to collect website content and metadata.

```bash
python crawler/selenium_crawler.py
```

or use the Scrapy spider.

---

### 2️⃣ Download PDFs

The processing pipeline automatically downloads PDFs discovered during crawling.

---

### 3️⃣ Create Embeddings and FAISS Index

Run:

```bash
python main.py
```

This will:

- Process website content
- Extract PDF text
- Clean documents
- Generate embeddings
- Create the FAISS vector database

---

## 💬 Running the Assistant

Launch Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## ❓ Example Queries

- 🎓 What is the fee structure of IIIT Una?
- 📅 Show the latest academic calendar.
- 📖 What are the admission requirements for M.Tech?
- 🕒 Give me the timetable for first-year students.
- 📢 What notices have been released recently?
- 🏠 What are the hostel rules?


---

### 📺 Demo Screenshot
[![Screen-Shot-2026-06-01-at-12-55-11.png](https://i.postimg.cc/sx5vyvct/Screen-Shot-2026-06-01-at-12-55-11.png)](https://postimg.cc/ct4sB1Pm)

[![Screenshot-(888).png](https://i.postimg.cc/GtRbFzFS/Screenshot-(888).png)](https://postimg.cc/r0h6c1YS)



## 🛠️ Tech Stack

### 🤖 AI & RAG

- Google Gemini 2.5 Flash
- LangChain
- FAISS

### 📊 Data Processing

- Python
- Pandas
- PDF Processing
- Text Cleaning

### 🌐 Web Scraping

- Scrapy
- Selenium

### 💻 Frontend

- Streamlit

---

## 🔄 Retrieval Pipeline

1. 🌐 Crawl IIIT Una website
2. 📄 Extract text, PDFs, tables, and images
3. 🧹 Clean and process content
4. 🧠 Generate embeddings
5. 📦 Store vectors in FAISS
6. 🔍 Retrieve relevant chunks
7. 🤖 Pass context to Gemini
8. ✅ Generate grounded responses

---

## ⚠️ Disclaimer

This project answers questions strictly from the indexed IIIT Una website and PDF documents. Responses are generated only from retrieved content and are intended to minimize hallucinations through Retrieval-Augmented Generation (RAG).

---

## 👨‍💻 Author

**Jitendra Singh**

🎓 M.Tech Student  
🤖 AI/ML Enthusiast  
🧠 Generative AI & RAG Developer


### ⭐⭐⭐ Star this repository if you found it useful!
