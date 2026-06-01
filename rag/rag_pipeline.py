import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

# --- INITIALIZE CLIENT GLOBALLY ONCE ---
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

# The global client instance stays open and accessible across Streamlit reruns
client = genai.Client(api_key=api_key)


def generate_answer(query, docs, verbose=True):
    context = "\n\n".join(doc.page_content for doc in docs)[:3000]

    if verbose:
        print(f"\nRetrieved docs: {len(docs)}")
        print("Sending request to Gemini...")

    prompt = f"""
You are a strict factual assistant for IIIT Una.

Rules:
- Answer only from the given context.
- Do not guess or add outside knowledge.
- If the answer is missing, say "I could not find this information."
- If the question is about a timetable, present it clearly.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        # Change 'get_client()' to use the global 'client' variable
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if verbose:
            print("Gemini responded successfully.")

        return (response.text or "").strip() or "I could not find this information."

    except Exception as error:
        if verbose:
            print("API error:", error)
        return f"Error generating answer: {error}"


# import os

# from dotenv import load_dotenv
# from google import genai


# load_dotenv()


# def get_client():
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

#     return genai.Client(api_key=api_key)


# def generate_answer(query, docs, verbose=True):
#     context = "\n\n".join(doc.page_content for doc in docs)[:3000]

#     if verbose:
#         print(f"\nRetrieved docs: {len(docs)}")
#         print("Sending request to Gemini...")

#     prompt = f"""
# You are a strict factual assistant for IIIT Una.

# Rules:
# - Answer only from the given context.
# - Do not guess or add outside knowledge.
# - If the answer is missing, say "I could not find this information."
# - If the question is about a timetable, present it clearly.

# Context:
# {context}

# Question:
# {query}

# Answer:
# """

#     try:
#         response = get_client().models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt,
#         )

#         if verbose:
#             print("Gemini responded successfully.")

#         return (response.text or "").strip() or "I could not find this information."

#     except Exception as error:
#         if verbose:
#             print("API error:", error)
#         return f"Error generating answer: {error}"
