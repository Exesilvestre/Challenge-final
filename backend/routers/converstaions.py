from fastapi import APIRouter, Depends, HTTPException
from services.conversations_service import update_conversation_name_service
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.schemas import ConversationCreate, ConversationResponse, ConversationUpdate
from services.conversations import create_conversation, delete_conversation, get_all_conversations, update_conversation
from utils.cohere_client import generate_response

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[ConversationResponse])  # List of ConversationResponse
async def get_conversations(db: Session = Depends(get_db)):
    conversations = get_all_conversations(db)
    return conversations

@router.post("/", response_model=ConversationResponse)
def create_new_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    print("llego")
    return create_conversation(db, conversation)

@router.delete("/{conversation_id}")
def delete_existing_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = delete_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted"}

# Modificar para aceptar un objeto con el nuevo nombre en el cuerpo de la solicitud
@router.put("/{conversation_id}")
def update_conversation_name(conversation_id: int, conversation_update: ConversationUpdate, db: Session = Depends(get_db)):
    conversation = update_conversation_name_service(db, conversation_id, conversation_update.new_name)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/generate")
def generate_message(prompt: str):
    response = generate_response(prompt)  # Llamar a la función que interactúa con Cohere
    return {"response": response}
