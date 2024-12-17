from langchain_core.tools import tool
import requests


@tool
def get_dolar_hoy():
    """
    Herramienta para consultar los valores actuales de los distintos tipos de dólar en Argentina.  

    Esta herramienta realiza una solicitud a la API de 'dolarapi.com' para obtener las cotizaciones actualizadas de las diferentes variantes del dólar disponibles en el país, incluyendo:  
    - Dólar oficial.  
    - Dólar blue.  
    - Dólar MEP.  
    - Dólar CCL (Contado con Liquidación).  
    - Dólar Tarjeta.
    - Dolar Mayorista.
    - Dolar Cripto.  

    Es ideal para quienes necesitan información confiable y al instante sobre el mercado cambiario en Argentina, ya sea para tomar decisiones financieras, planificar viajes, o realizar operaciones de compra/venta de divisas.  

    Args:
        None.

    Returns:
        str: Una descripción en formato de texto con las cotizaciones actuales de los diferentes tipos de dólar o un mensaje de error si ocurre algún problema al realizar la consulta.
    """
    url = 'https://dolarapi.com/v1/dolares'
    try:
        response = requests.get(url)
        response.raise_for_status()
        dolar_data = response.json()
        return f"Dólar hoy: {dolar_data}"
    except requests.RequestException as e:
        return f"Error al obtener información del dólar: {str(e)}"