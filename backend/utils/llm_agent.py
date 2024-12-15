import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import requests
from langchain_core.tools import tool
from langchain_cohere import ChatCohere 
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor

# Cargar variables de entorno si es necesario
load_dotenv()

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
class DolarSearchInput(BaseModel):
    query: str = Field(description="Consulta para buscar información sobre el dólar")

# Función para obtener la respuesta del modelo
def get_llm_response(input_text: str) -> str:
    # Definir el LLM de Cohere
    llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"), 
                     model="command-r-plus-08-2024", 
                     temperature=0)

    # Preambulo
    preamble = """
    You are an expert who answers the user's question with the most relevant datasource. You are equipped with an internet search tool and a special vectorstore of information about how to write good essays.
    """
    
    # Crear el prompt de conversación
    prompt = ChatPromptTemplate.from_template("{input}")

    # Crear el agente ReAct
    agent = create_cohere_react_agent(
        llm=llm,
        tools=[get_dolar_hoy],
        prompt=prompt,
    )
    
    # Crear la entrada para el agente como un diccionario
    query_input = DolarSearchInput(query=input_text)  # Creamos la instancia de DolarSearchInput
    
    # Ejecutar el agente con el input proporcionado
    agent_executor = AgentExecutor(agent=agent, tools=[get_dolar_hoy], verbose=True)
    
    # Obtener la respuesta
    response = agent_executor.invoke({
        "input": query_input.query,  # Pasamos la consulta del modelo
        "preamble": preamble,
    })
    
    return response['output']
