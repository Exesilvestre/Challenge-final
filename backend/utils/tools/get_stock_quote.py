from dotenv import load_dotenv
import requests
from langchain_core.tools import tool
import os

load_dotenv()
@tool
def get_stock_quote(symbol: str) -> str:
    """
    Herramienta para obtener la cotización de una acción utilizando su símbolo en la API de Alpha Vantage.  
    Dado un símbolo, devuelve la cotización actual de la acción.

    Args:
        symbol (str): El símbolo de la acción para la cual se desea obtener la cotización.

    Returns:
        str: La cotización de la acción o un mensaje de error si ocurre un problema al realizar la consulta.
    """
    api_key = os.getenv("ALPGA_API_KEY")  # Reemplaza con tu propia clave API de Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Verificamos si los datos están disponibles
        if 'Time Series (5min)' in data:
            # Tomamos la cotización más reciente
            last_time = list(data['Time Series (5min)'].keys())[0]
            last_quote = data['Time Series (5min)'][last_time]
            price = last_quote['4. close']
            return f"La cotización más reciente de {symbol} es {price} USD."
        else:
            return f"No se pudo obtener la cotización para el símbolo {symbol}."
    except requests.RequestException as e:
        return f"Error al obtener la cotización de {symbol}: {str(e)}"