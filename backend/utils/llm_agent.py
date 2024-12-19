import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_cohere import ChatCohere
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from utils.tools.get_dolar import get_dolar_hoy
from utils.tools.get_stock_quote import get_stock_quote
from utils.tools.get_symbol_company import get_symbol_for_company
from utils.tools.search_vector_db import search_vector_db

load_dotenv()

# Definir el esquema de entrada para la herramienta de búsqueda
class SearchInput(BaseModel):
    query: str = Field(description="Consulta para buscar información sobre el dólar")

# Función para obtener la respuesta del modelo
def get_llm_response(input_text: str, history: str) -> str:
    # Definir el LLM de Cohere
    llm = ChatCohere(cohere_api_key=os.getenv("COHERE_API_KEY"), 
                     model="command-r-plus-08-2024", 
                     temperature=0,
                     max_tokens=600
                     )

    # Preambulo
    preamble = """
    Eres un asistente de IA especializado en finanzas personales e inversiones. 
    Tienes acceso a una base de datos vectorial que contiene información detallada sobre finanzas personales e inversiones,
    Tienes una herramienta que te permite obtener el precio actual del dólar.
    Tienes herramientas para obtener el precio de las acciones de empresas.

    Al responder:
    1. Utiliza la información más relevante de la base de datos vectorial como fuente principal para temas relacionados con finanzas e inversiones.
    2. Prioriza la precisión y la claridad en tus respuestas, citando la fuente de datos o herramientas cuando sea relevante.
    3. Responde de forma concisa, resumida y entendible para personas no expertas en finanzas.
    4. Si el usuario pregunta por un tema que no sea de finanzas,
      reponde comunicandole cual es tu especialdiad, pero si puedes repsonder saludos.
    5. Si el usuario pide una recomendacion de inversion 
    puedes repsonder pero aclara que consulte a un especialista
    
    Solo debes responder consultas relacionadas a las finanzas e inversiones.
    Si no encuentras información adecuada en las fuentes disponibles, sé transparente y comunícalo al usuario en lugar de inventar una respuesta.
    """
    
    # Crear el prompt de conversación
    prompt = ChatPromptTemplate.from_template(
        f"""
        ###
        Instrucciones: 
        - El idioma de la respuesta debe ser en español.
        - Deben ser respuestas resumidas, extenderse maximo 6 oraciones.

        ### 
        Historia:
        {history}
        
        Usuario:
        {input_text}

        """
    )

    # Crear el agente ReAct
    agent = create_cohere_react_agent(
        llm=llm,
        tools=[get_dolar_hoy, search_vector_db, get_symbol_for_company, get_stock_quote],
        prompt=prompt,
    )
    
    # Crear la entrada para el agente como un diccionario
    query_input = SearchInput(query=input_text)  # Creamos la instancia de SearchInput

    # Ejecutar el agente con el input proporcionado
    agent_executor = AgentExecutor(agent=agent, tools=[get_dolar_hoy, search_vector_db, get_symbol_for_company, get_stock_quote], verbose=True)

    response = agent_executor.invoke({
        "preamble": preamble,
        "input": query_input.query
    })

    return response.get('output', 'No output generated')