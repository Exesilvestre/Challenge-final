from langchain_chroma import Chroma
from langchain_cohere import CohereEmbeddings


perisent_directory = "./data/chromadb"
collection_name= "collection"
embeddings_functions = CohereEmbeddings(model='embed-multilingual-v3.0')

def chroma_config():
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings_functions,
        persist_directory=perisent_directory
    )
    return vector_store