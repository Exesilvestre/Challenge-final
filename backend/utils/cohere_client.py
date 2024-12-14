from dotenv import load_dotenv
import os
import cohere

class CohereClient:
    def __init__(self):
        # Cargar el archivo .env y obtener la clave API
        load_dotenv()  
        self.api_key = "oLzddANOIqbvK7TieI6rtnAgV0PkpvxNVGlfcqL5"
        
        if not self.api_key:
            raise ValueError("COHERE_API_KEY no está configurada en el archivo .env")
        
        # Crear una instancia del cliente de Cohere
        self.client = cohere.Client(self.api_key)

    def chat(self, messages):
        """
        Envía un conjunto de mensajes al modelo de Cohere y obtiene una respuesta.
        :param messages: Lista de diccionarios con el formato {'role': 'user', 'content': 'message'}
        :return: Respuesta del modelo de Cohere
        """
        response = self.client.chat(
            model="command-r-plus-08-2024",  # Puedes personalizar el modelo si es necesario
            messages=messages
        )
        return response