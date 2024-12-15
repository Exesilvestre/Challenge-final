from fastapi import APIRouter, Depends, HTTPException
from services.conversations_service import (
    update_conversation_name_service,
    create_conversation_service,
    delete_conversation_service,
    get_all_conversations_service,
    generate_message_service,
)
from sqlalchemy.orm import Session
from models.database import Conversation, Message, SessionLocal
from models.schemas import ConversationCreate, ConversationResponse, ConversationUpdate, MessagePrompt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ConversationResponse])
async def get_conversations(db: Session = Depends(get_db)):
    return get_all_conversations_service(db)

@router.post("/", response_model=ConversationResponse)
def create_new_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    return create_conversation_service(db, conversation)

@router.delete("/{conversation_id}")
def delete_existing_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = delete_conversation_service(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted"}

@router.put("/{conversation_id}")
def update_conversation_name(conversation_id: int, conversation_update: ConversationUpdate, db: Session = Depends(get_db)):
    conversation = update_conversation_name_service(db, conversation_id, conversation_update.new_name)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/generate/{conversation_id}")
def generate_message(conversation_id: int, prompt: MessagePrompt, db: Session = Depends(get_db)):
    try:
        return generate_message_service(db, conversation_id, prompt.prompt)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error en generate_message_service: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}/messages")
async def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages