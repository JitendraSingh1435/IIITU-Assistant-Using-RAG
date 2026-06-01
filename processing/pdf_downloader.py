

import os
import requests
from tqdm import tqdm

def download_pdfs(data):
    os.makedirs("data/pdfs", exist_ok=True)

    pdf_urls = [
        item.get("url", "")
        for item in data
        if item.get("url", "").lower().endswith(".pdf")
    ]

    for url in tqdm(pdf_urls, desc="⬇️ Downloading PDFs"):
        try:
            filename = url.split("/")[-1]
            filepath = os.path.join("data/pdfs", filename)

            if os.path.exists(filepath):
                continue

            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)

        except Exception as e:
            print(f"❌ Error downloading {url}: {e}")



























# import os
# import requests

# def download_pdfs(data):
#     os.makedirs("data/pdfs", exist_ok=True)

#     for item in data:
#         url = item.get("url", "")

#         # ✅ Check if URL itself is a PDF
#         if url.lower().endswith(".pdf"):
#             try:
#                 filename = url.split("/")[-1]
#                 filepath = os.path.join("data/pdfs", filename)

#                 if not os.path.exists(filepath):
#                     print(f"⬇️ Downloading: {filename}")
#                     response = requests.get(url, timeout=10)
#                     with open(filepath, "wb") as f:
#                         f.write(response.content)

#             except Exception as e:
#                 print(f"❌ Error downloading {url}: {e}")














# import os
# import requests


# def download_pdfs(json_data, save_folder="data/pdfs"):
#     os.makedirs(save_folder, exist_ok=True)

#     downloaded = set()

#     for item in json_data:
#         pdf_links = item.get("pdfs", [])

#         for url in pdf_links:
#             if url and url.endswith(".pdf") and url not in downloaded:
#                 try:
#                     filename = url.split("/")[-1]
#                     filepath = os.path.join(save_folder, filename)

#                     print(f"⬇️ Downloading: {filename}")

#                     response = requests.get(url, timeout=10)
#                     with open(filepath, "wb") as f:
#                         f.write(response.content)

#                     downloaded.add(url)

#                 except Exception as e:
#                     print("Download error:", e)