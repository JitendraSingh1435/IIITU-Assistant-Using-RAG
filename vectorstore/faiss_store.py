


from langchain.vectorstores import FAISS
from tqdm import tqdm
import os
import pickle


FAISS_PATH = "faiss_index"
EMBED_CACHE = "data/processed/embeddings.pkl"


def create_faiss(docs, embedding_model):
    os.makedirs("data/processed", exist_ok=True)

    texts = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]

    # ✅ LOAD EXISTING EMBEDDINGS (RESUME)
    if os.path.exists(EMBED_CACHE):
        print("📦 Loading saved embeddings...")
        with open(EMBED_CACHE, "rb") as f:
            embeddings = pickle.load(f)
    else:
        embeddings = []

    start_idx = len(embeddings)

    print(f"🔢 Total docs: {len(texts)} | Already embedded: {start_idx}")

    # ✅ BATCH EMBEDDING WITH PROGRESS BAR
    batch_size = 64

    for i in tqdm(range(start_idx, len(texts), batch_size), desc="🧠 Creating embeddings"):
        batch = texts[i:i+batch_size]

        emb = embedding_model.embed_documents(batch)
        embeddings.extend(emb)

        # ✅ SAVE PROGRESS AFTER EACH BATCH
        with open(EMBED_CACHE, "wb") as f:
            pickle.dump(embeddings, f)

    # ✅ CREATE FAISS
    print("📦 Building FAISS index...")
    pairs = list(zip(texts, embeddings))

    vectorstore = FAISS.from_embeddings(
        pairs,
        embedding_model,
        metadatas=metadatas
    )
    # vectorstore = FAISS.from_embeddings(
    #     embeddings,
    #     embedding_model,
    #     metadatas=metadatas
    # )

    vectorstore.save_local(FAISS_PATH)

    return vectorstore


def load_faiss(embedding_model):
    return FAISS.load_local(
        FAISS_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )




























# from langchain.vectorstores import FAISS


# def create_faiss(docs, embedding_model):
#     texts = [doc.page_content for doc in docs]

#     vectorstore = FAISS.from_texts(texts, embedding_model)

#     vectorstore.save_local("faiss_index")

#     return vectorstore


# def load_faiss(embedding_model):
#     return FAISS.load_local(
#         "faiss_index",
#         embedding_model,
#         allow_dangerous_deserialization=True
#     )