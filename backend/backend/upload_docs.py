import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DATA_FOLDER = "data"
VECTOR_FOLDER = "vector_db"


all_documents = []


# Read all PDF files
for filename in os.listdir(DATA_FOLDER):

    if filename.lower().endswith(".pdf"):

        file_path = os.path.join(
            DATA_FOLDER,
            filename
        )

        print(f"Loading: {filename}")

        loader = PyPDFLoader(file_path)

        documents = loader.load()

        all_documents.extend(documents)


print(f"Total pages loaded: {len(all_documents)}")


# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(
    all_documents
)

print(f"Total chunks created: {len(chunks)}")


# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=VECTOR_FOLDER
)


print("================================")
print("Vector database created!")
print("================================")