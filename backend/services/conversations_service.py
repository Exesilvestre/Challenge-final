# services/conversation_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.database import Conversation, Message
from models.schemas import ConversationCreate
from utils.agent import llm_final_response
from utils.llm_agent import get_llm_response


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
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = Message(content=prompt, role="user", conversation_id=conversation_id)
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Obtener el historial de la conversación
    conversation_history = get_conversation_history(db, conversation_id)

    # Crear la historia de la conversación apra el modelo
    history = "\n".join([f"{message['role']}: {message['content']}" for message in conversation_history])

    # Llamar a la función llm_final_response para generar la respuesta
    try:
        llm_response = get_llm_response(prompt, history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en LLM: {str(e)}")
    
    # Guardar la respuesta final en la base de datos
    assistant_message = Message(content=llm_response, role="assistant", conversation_id=conversation_id)
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    return {"response": llm_response}

def get_conversation_history(db: Session, conversation_id: int):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.id.desc()).limit(4).all()
    return [{"role": message.role, "content": message.content} for message in reversed(messages)]