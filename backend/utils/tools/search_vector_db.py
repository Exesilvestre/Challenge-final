from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_cohere import CohereEmbeddings, CohereRerank
from langchain_core.tools import tool
from utils.chroma_config import chroma_config
from langchain.retrievers import ContextualCompressionRetriever


def create_query_embedding(query_text):
    load_dotenv()

    cohere_embeddings = CohereEmbeddings(model='embed-multilingual-v3.0')
    # Embedding the query text
    query_embedding = cohere_embeddings.embed_query(query_text)

    return query_embedding


# Cargar variables de entorno si es necesario
load_dotenv()
    
rerank_model = "rerank-multilingual-v3.0"
# Crear la herramienta para consultar Chroma
@tool
def search_vector_db(query: str):
    """
    Herramienta para realizar búsquedas en una base de datos vectorial especializada en temas de finanzas personales y generales, con un enfoque en Argentina.  

    Esta base de datos contiene información clave sobre cómo manejar tus gastos, planificar presupuestos, e invertir de manera inteligente. Además, incluye contenido detallado sobre herramientas financieras disponibles en el país, tales como:  
    - Qué son y cómo funcionan los CEDEARs.  
    - Fondos comunes de inversión (FCI).  
    - Criptomonedas y sus riesgos.  
    - Plazos fijos.  
    - Otros instrumentos financieros disponibles para pequeñas y grandes inversiones.  

    También aborda conceptos financieros fundamentales que cualquier persona interesada en mejorar su situación económica puede usar, con un enfoque adaptado al contexto argentino.  

    Args:
        query (str): La consulta o tema que deseas buscar en la base de datos.

    Returns:
        str: Documentos o información relevante relacionada con la consulta realizada.
    """
    query_embedding = create_query_embedding(query)
    vector_store = chroma_config()
    raw_results = vector_store.similarity_search_by_vector(
        embedding=query_embedding,
        k=1  # Recuperar más documentos para mejorar el rerank
    )
    print(raw_results)

    if not raw_results:
        raise HTTPException(status_code=404, detail="No results found")

    reranker = CohereRerank(model=rerank_model)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=vector_store.as_retriever()
    )
    reranked_docs = compression_retriever.get_relevant_documents(query)
    return reranked_docs[0].page_content