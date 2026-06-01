# class CustomRetriever:
#     def __init__(self, vectorstore, k=5):
#         self.retriever = vectorstore.as_retriever(search_kwargs={"k": k})

#     def get_docs(self, query):
#         return self.retriever.get_relevant_documents(query)


class CustomRetriever:
    def __init__(self, vectorstore, k=16):
        self.vectorstore = vectorstore
        self.k = k

    def get_docs(self, query):
        # 🔍 Basic semantic search
        docs = self.vectorstore.similarity_search(query, k=self.k)

        # 🎯 Optional: prioritize timetable-related chunks
        if "timetable" in query.lower() or "schedule" in query.lower():
            # docs = sorted(
            #     docs,
            #     key=lambda x: "table" in x.page_content.lower(),
            #     reverse=True
            # )

            docs = self.vectorstore.similarity_search(
                query,
                k=self.k,
                filter={"type": "table"}
            )

        return docs