import os
import glob
import time
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.schema import Document
from pypdf import PdfReader
from utils.chroma_config import chroma_config

def create_chunk_embedding():
    load_dotenv()

    # Asegúrate de que la variable de entorno COHERE_API_KEY esté definida en tu archivo .env
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("Falta la clave de API de Cohere en las variables de entorno.")

    # Ruta al directorio que contiene los archivos PDF
    pdf_directory = './data'

    # Inicializa Chroma vector store con el directorio dado y el nombre de colección
    vectorstore = chroma_config()

    # Crea el separador de texto (text splitter)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

    # Total de caracteres procesados
    total_characters = 0

    # Itera sobre todos los archivos PDF en el directorio y sus subdirectorios
    pdf_files = glob.glob(os.path.join(pdf_directory, '**/*.pdf'), recursive=True)
    print(pdf_files)

    for pdf_file in pdf_files:
        print(f"Procesando {pdf_file}")
        
        # Carga el PDF y extrae el texto utilizando PDFReader
        with open(pdf_file, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

        # Limpia el texto (elimna saltos de línea y espacios extra)
        text = text.replace('\n', ' ').strip()

        # Cuenta los caracteres del texto extraído
        total_characters += len(text)

        # Divide el texto en chunks
        documents = [Document(page_content=text, metadata={"source": pdf_file})]  # Aquí usamos todo el texto como un solo documento
        chunks = text_splitter.split_documents(documents)

        # Embebe cada chunk y añádelo al vector store
        for chunk in chunks:
            # Convierte el chunk en un objeto Document para compatibilidad con Chroma
            doc = Document(page_content=chunk.page_content, metadata=chunk.metadata)

            # Añade al vector store
            vectorstore.add_documents([doc])

            # Espera 1 segundo entre cada llamada a la API (ajustar según sea necesario)
            time.sleep(5)  # 1 segundo de espera entre llamadas

    # Imprime el total de caracteres procesados
    print(f"Total de caracteres procesados: {total_characters}")

    print("Base de datos 'finanzas' creada y guardada.")

if __name__ == "__main__":
    create_chunk_embedding()
