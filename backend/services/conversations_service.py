from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.database import Conversation, Message
from models.schemas import ConversationCreate

def create_conversation(db: Session, conversation_data: ConversationCreate):
    # Verificar si ya existe una conversación con el mismo nombre
    existing_conversation = db.query(Conversation).filter(Conversation.name == conversation_data.name).first()
    if existing_conversation:
        raise HTTPException(status_code=400, detail="Conversation with this name already exists")
    
    # Crear una nueva conversación, el id se genera automáticamente
    conversation = Conversation(name=conversation_data.name)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)  # Esto recarga el objeto con los cambios de la base de datos, como el id auto-generado

    return conversation

def delete_conversation(db: Session, conversation_id: int):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        return None  # Si no existe la conversación, devolvemos None
    
    db.delete(conversation)
    db.commit()
    return conversation

def update_conversation_name_service(db: Session, conversation_id: int, new_name: str):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        return None  # Si no existe la conversación, devolvemos None
    
    # Verificar si ya existe una conversación con el nuevo nombre
    if db.query(Conversation).filter(Conversation.name == new_name).first():
        raise HTTPException(status_code=400, detail="Conversation with this name already exists")

    conversation.name = new_name
    db.commit()
    db.refresh(conversation)
    return conversation


def get_all_conversations(db: Session):
    """
    Retrieve all conversations from the database.
    """
    return db.query(Conversation).all()