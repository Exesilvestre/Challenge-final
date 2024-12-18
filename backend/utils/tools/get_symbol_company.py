from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
import os

load_dotenv()

@tool
def get_symbol_for_company(company_name: str) -> str:
    """
    Herramienta para buscar el símbolo de una empresa utilizando la API de Alpha Vantage.  
    Dado el nombre de la empresa, devuelve el símbolo correspondiente.

    Args:
        company_name (str): El nombre de la empresa que se desea buscar.

    Returns:
        str: El símbolo de la empresa o un mensaje de error si ocurre un problema al realizar la consulta.
    """
    api_key = os.getenv("ALPGA_API_KEY")  # Reemplaza con tu propia clave API de Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Comprobamos si hay resultados
        if 'bestMatches' in data and len(data['bestMatches']) > 0:
            # Obtenemos el primer resultado
            symbol = data['bestMatches'][0]['1. symbol']
            return f"El símbolo de {company_name} es {symbol}."
        else:
            return f"No se encontraron resultados para la empresa {company_name}."
    except requests.RequestException as e:
        return f"Error al obtener el símbolo de la empresa: {str(e)}"
