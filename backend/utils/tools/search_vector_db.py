from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_cohere import CohereEmbeddings, CohereRerank
from langchain_core.tools import tool
import numpy as np
from utils.chroma_config import chroma_config
from langchain.retrievers import ContextualCompressionRetriever


# Cargar variables de entorno si es necesario
load_dotenv()
    
rerank_model = "rerank-v3.5"
# Crear la herramienta para consultar Chroma
@tool
def search_vector_db(query: str):
    """
    Herramienta para realizar búsquedas en una base de datos vectorial especializada en temas de finanzas personales y generales, con un enfoque en Argentina.  

    Esta base de datos contiene información clave sobre cómo manejar tus gastos, planificar presupuestos, e invertir de manera inteligente. Además, incluye contenido detallado sobre herramientas financieras disponibles en el país, tales como:   
    - Fondos comunes de inversión (FCI).  
    - Criptomonedas y sus riesgos.  
    - Plazos fijos.  
    - Bonos de inversion.  

    También aborda conceptos financieros fundamentales que cualquier persona interesada en mejorar su situación económica puede usar, con un enfoque adaptado al contexto argentino.  

    Args:
        query (str): La consulta o tema que deseas buscar en la base de datos.

    Returns:
        str: Documentos o información relevante relacionada con la consulta realizada.
    """
    vector_store = chroma_config()

    reranker = CohereRerank(model=rerank_model)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=vector_store.as_retriever(),
        compression_threshold=0.2,
        search_kwargs={'k': 4}
    )
    
    # Rerank de los 5 primeros documentos
    reranked_docs = compression_retriever.get_relevant_documents(query)
    print(f"Documentos después de rerank: {reranked_docs}")

    # Calcular similitudes para cada uno de los 5 documentos
    similarities = []
    for doc in reranked_docs:
        relevance_score = doc.metadata.get("relevance_score", None)
        if relevance_score:
            similarities.append(relevance_score)
        else:
            # Si no hay puntuación de similitud en los metadatos, usa la distancia
            similarities.append(np.nan)  # Valor NaN en caso de que no haya score

    # Mostrar las similitudes de todos los resultados
    for i, doc in enumerate(reranked_docs):
        print(f"Doc {i+1}: Similitud: {similarities[i]}")
    
    # Seleccionar los 2 documentos más similares
    sorted_indices = np.argsort(similarities)[::-1]  # Ordenar los documentos por similitud (de mayor a menor)
    best_docs = [reranked_docs[i] for i in sorted_indices[:2]]  # Tomar los 2 mejores

    # Mostrar el contenido de los dos documentos seleccionados
    print("Mejores documentos seleccionados:")
    for doc in best_docs:
        print(f"Documento seleccionado: {doc.page_content[:200]}...")

    return best_docs  # Retornar los 2 documentos más relevantes