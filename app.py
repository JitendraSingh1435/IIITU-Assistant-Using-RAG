import streamlit as st

from main import get_retriever
from rag.rag_pipeline import generate_answer


st.set_page_config(
    page_title="IIIT Una RAG Assistant",
    layout="wide",
)


def render_sources(docs):
    if not docs:
        st.info("No source documents were retrieved for this question.")
        return

    with st.expander("Retrieved sources", expanded=False):
        for index, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "Unknown source")
            doc_type = doc.metadata.get("type", "unknown")
            snippet = doc.page_content[:500].strip()

            st.markdown(f"**{index}. {source}**")
            st.caption(f"Type: {doc_type}")
            if snippet:
                st.text(snippet)


st.title("IIIT Una RAG Assistant")
st.write("Ask questions over the indexed website and PDF content.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Retrieved documents", min_value=3, max_value=12, value=8)
    show_sources = st.checkbox("Show retrieved sources", value=True)
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# --- METHOD 1 IMPLEMENTATION START ---
# Store retriever in session state so clients do not get closed or re-initialized
if "retriever" not in st.session_state:
    with st.spinner("Loading embeddings and FAISS index..."):
        st.session_state.retriever = get_retriever(k=top_k)
else:
    # Update k value dynamically if the user updates the slider
    st.session_state.retriever.k = top_k
# --- METHOD 1 IMPLEMENTATION END ---

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and show_sources:
            render_sources(message.get("docs", []))

prompt = st.chat_input("Ask about admissions, timetables, notices, or PDFs...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            # Use the persistent retriever from session state
            retriever = st.session_state.retriever
            docs = retriever.get_docs(prompt)
            answer = generate_answer(prompt, docs, verbose=False)

        st.markdown(answer)
        if show_sources:
            render_sources(docs)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "docs": docs,
        }
    )


# import streamlit as st

# from main import get_retriever
# from rag.rag_pipeline import generate_answer


# st.set_page_config(
#     page_title="IIIT Una RAG Assistant",
#     layout="wide",
# )


# @st.cache_resource(show_spinner="Loading embeddings and FAISS index...")
# def load_retriever(top_k):
#     return get_retriever(k=top_k)


# def render_sources(docs):
#     if not docs:
#         st.info("No source documents were retrieved for this question.")
#         return

#     with st.expander("Retrieved sources", expanded=False):
#         for index, doc in enumerate(docs, start=1):
#             source = doc.metadata.get("source", "Unknown source")
#             doc_type = doc.metadata.get("type", "unknown")
#             snippet = doc.page_content[:500].strip()

#             st.markdown(f"**{index}. {source}**")
#             st.caption(f"Type: {doc_type}")
#             if snippet:
#                 st.text(snippet)


# st.title("IIIT Una RAG Assistant")
# st.write("Ask questions over the indexed website and PDF content.")

# with st.sidebar:
#     st.header("Settings")
#     top_k = st.slider("Retrieved documents", min_value=3, max_value=12, value=8)
#     show_sources = st.checkbox("Show retrieved sources", value=True)
#     if st.button("Clear chat"):
#         st.session_state.messages = []
#         st.rerun()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         if message["role"] == "assistant" and show_sources:
#             render_sources(message.get("docs", []))

# prompt = st.chat_input("Ask about admissions, timetables, notices, or PDFs...")

# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         with st.spinner("Searching the knowledge base..."):
#             retriever = load_retriever(top_k)
#             docs = retriever.get_docs(prompt)
#             answer = generate_answer(prompt, docs, verbose=False)

#         st.markdown(answer)
#         if show_sources:
#             render_sources(docs)

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": answer,
#             "docs": docs,
#         }
#     )
