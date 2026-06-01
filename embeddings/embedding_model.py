
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "batch_size": 64,   # you can try 64 carefully
            "normalize_embeddings": True
        }
    )















# from sentence_transformers import SentenceTransformer

# def get_embedding_model():
#     return SentenceTransformer("all-MiniLM-L6-v2")