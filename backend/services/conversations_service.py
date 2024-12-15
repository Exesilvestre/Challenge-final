from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.database import Conversation, Message
from models.schemas import ConversationCreate
from utils.cohere_client import CohereClient

def create_conversation_service(db: Session, conversation_data: ConversationCreate):
    existing_conversation = db.query(Conversation).filter(Conversation.name == conversation_data.name).first()
    if existing_conversation:
        raise HTTPException(status_code=400, detail="Conversation with this name already exists")
    
    conversation = Conversation(name=conversation_data.name)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def delete_conversation_service(db: Session, conversation_id: int):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        return None
    
    db.delete(conversation)
    db.commit()
    return conversation

def update_conversation_name_service(db: Session, conversation_id: int, new_name: str):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        return None
    
    if db.query(Conversation).filter(Conversation.name == new_name).first():
        raise HTTPException(status_code=400, detail="Conversation with this name already exists")

    conversation.name = new_name
    db.commit()
    db.refresh(conversation)
    return conversation

def get_all_conversations_service(db: Session):
    return db.query(Conversation).all()

def generate_message_service(db: Session, conversation_id: int, prompt: str):
    # Verificar si la conversación existe
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Guardar el mensaje del usuario
    user_message = Message(content=prompt, role="user", conversation_id=conversation_id)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Generar la respuesta
    cohere_client = CohereClient()
    response_content = cohere_client.generate_text(prompt, max_tokens=100)

    # Guardar la respuesta del asistente
    assistant_message = Message(content=response_content, role="assistant", conversation_id=conversation_id)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": response_content}


def get_messages_service(db: Session, conversation_id: int):
    # Verificar si la conversación existe
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Obtener los mensajes de la conversación
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages