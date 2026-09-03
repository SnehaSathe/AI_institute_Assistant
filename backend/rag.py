from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


db = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)


def retrieve_context(question, score_threshold=1.5):

    results = db.similarity_search_with_score(
        question,
        k=3
    )

    # Chroma returns (document, distance) pairs — lower distance
    # means more similar. Keep only chunks below the threshold.
    relevant_docs = [
        doc for doc, score in results
        if score <= score_threshold
    ]

    if not relevant_docs:
        return "No relevant information found in institute documents."

    context = "\n\n".join(
        doc.page_content
        for doc in relevant_docs
    )

    return context