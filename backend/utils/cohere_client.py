from dotenv import load_dotenv
import os
import cohere

class CohereClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("COHERE_API_KEY")  
        
        if not self.api_key:
            raise ValueError("COHERE_API_KEY no está configurada en el archivo .env o en el entorno")
        
        # Inicializar el cliente de Cohere
        self.client = cohere.Client(self.api_key)

    def chat(self, messages: list[dict]) -> str:
        """
        Envía un conjunto de mensajes al modelo de Cohere y obtiene una respuesta.
        
        :param messages: Lista de diccionarios con el formato {'role': 'user', 'content': 'message'}
        :return: Respuesta del modelo de Cohere como texto
        """
        try:
            response = self.client.chat(
                model="command-r-plus-08-2024",  # Modelo predeterminado
                messages=messages
            )
            return response.text
        except cohere.CohereError as e:
            raise ValueError(f"Error al comunicarse con Cohere: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")

    def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        """
        Genera texto basado en un prompt utilizando Cohere.

        :param prompt: Texto inicial para que el modelo continúe.
        :param max_tokens: Número máximo de tokens en la respuesta.
        :return: Texto generado.
        """
        try:
            response = self.client.generate(
                model="command-r-plus-08-2024",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.generations[0].text
        except cohere.CohereError as e:
            raise ValueError(f"Error al generar texto: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")

    def summarize(self, text: str) -> str:
        """
        Genera un resumen del texto dado.

        :param text: Texto que se desea resumir.
        :return: Resumen generado.
        """
        try:
            response = self.client.summarize(
                model="summarize-xlarge",
                text=text
            )
            return response.summary
        except cohere.CohereError as e:
            raise ValueError(f"Error al resumir texto: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error inesperado: {str(e)}")
