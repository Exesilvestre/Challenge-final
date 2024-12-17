import os
import cohere
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel, Field
import requests
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_cohere import ChatCohere, CohereEmbeddings 
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain_community.vectorstores import Chroma

from utils.chroma_config import chroma_config

def create_query_embedding(query_text):
    load_dotenv()

    cohere_embeddings = CohereEmbeddings(model='embed-multilingual-v3.0')
    # Embedding the query text
    query_embedding = cohere_embeddings.embed_query(query_text)

    return query_embedding


# Cargar variables de entorno si es necesario
load_dotenv()
    
perisent_directory = "../data/chromadb"
collection_name= "finanzas"
embeddings_functions = CohereEmbeddings(model='embed-multilingual-v3.0')
# Crear la herramienta para consultar Chroma
@tool
def search_vector_db(query: str):
    """
    Herramienta para consultar la base de datos vectorial de Chroma.
    
    Args:
        query (str): La consulta para buscar en la base de datos.
    
    Returns:
        str: Los documentos relevantes encontrados.
    """
    query_embedding = create_query_embedding(query)
    vector_store = chroma_config()
    print(vector_store.get())
    results = vector_store.similarity_search_by_vector(
        embedding=query_embedding,
        k=1
    )
    print(results)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")

    return results[0].page_content

# Función que obtiene el valor del dólar hoy
@tool
def get_dolar_hoy():
    """
    Fetches the current exchange rate for the dollar from the API.
    This function makes a GET request to the 'dolarapi.com' API to retrieve
    the current exchange rate data.

    Returns:
        str: A string containing the current exchange rate of the dollar or an error message.
    """
    url = 'https://dolarapi.com/v1/dolares'
    try:
        response = requests.get(url)
        response.raise_for_status()
        dolar_data = response.json()
        return f"Dólar hoy: {dolar_data}"
    except requests.RequestException as e:
        return f"Error al obtener información del dólar: {str(e)}"

# Definir el esquema de entrada para la herramienta de búsqueda
class SearchInput(BaseModel):
    query: str = Field(description="Consulta para buscar información sobre el dólar")

# Función para obtener la respuesta del modelo
def get_llm_response(input_text: str) -> str:
    # Definir el LLM de Cohere
    llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"), 
                     model="command-r-plus-08-2024", 
                     temperature=0)

    # Preambulo
    preamble = """
    Sos un asistente de IA que responde al usuario utilizando la fuente dee datos mas relevantes, podes acceder al base de datos vectorial para temas de finanzas y al preciod el dolar usando la API.
    """
    
    # Crear el prompt de conversación
    prompt = ChatPromptTemplate.from_template("{input}")

    # Crear el agente ReAct
    agent = create_cohere_react_agent(
        llm=llm,
        tools=[get_dolar_hoy, search_vector_db],
        prompt=prompt,
    )
    
    # Crear la entrada para el agente como un diccionario
    query_input = SearchInput(query=input_text)  # Creamos la instancia de DolarSearchInput
    
    # Ejecutar el agente con el input proporcionado
    agent_executor = AgentExecutor(agent=agent, tools=[get_dolar_hoy, search_vector_db], verbose=True)
    
    # Obtener la respuesta
    response = agent_executor.invoke({
        "input": query_input.query,  # Pasamos la consulta del modelo
        "preamble": preamble,
    })
    
    return response['output']
